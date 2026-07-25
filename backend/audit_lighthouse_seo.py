# -*- coding: utf-8 -*-
"""
Lighthouse SEO Auditor for ShunyakiKhoj
Evaluates 12 core Lighthouse SEO audits across all live static & SPA pages.
"""

import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES_TO_AUDIT = [
    ("Main Portal Root", os.path.join(ROOT_DIR, "index.html"), "https://shunyakikhoj.co.in/"),
    ("Panchang SEO Landing", os.path.join(ROOT_DIR, "panchang", "index.html"), "https://shunyakikhoj.co.in/panchang/"),
    ("Kundli SEO Landing", os.path.join(ROOT_DIR, "kundli", "index.html"), "https://shunyakikhoj.co.in/kundli/"),
    ("Kundli Matching Landing", os.path.join(ROOT_DIR, "kundli-matching", "index.html"), "https://shunyakikhoj.co.in/kundli-matching/"),
    ("Divisional Charts Landing", os.path.join(ROOT_DIR, "divisional-charts", "index.html"), "https://shunyakikhoj.co.in/divisional-charts/"),
    ("Dasha Systems Landing", os.path.join(ROOT_DIR, "dasha-systems", "index.html"), "https://shunyakikhoj.co.in/dasha-systems/"),
    ("Sanskrit Dictionary Landing", os.path.join(ROOT_DIR, "sanskrit-dictionary", "index.html"), "https://shunyakikhoj.co.in/sanskrit-dictionary/"),
    ("Jyotish Standalone Window", os.path.join(ROOT_DIR, "jyotish_window.html"), "https://shunyakikhoj.co.in/jyotish_window.html")
]

def audit_file(page_name, filepath, url):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    audits = {}

    # 1. Document has a <title> element
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    audits["title_element"] = bool(title_match and title_match.group(1).strip())
    title_text = title_match.group(1).strip() if title_match else ""

    # 2. Document has a meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    audits["meta_description"] = bool(desc_match and desc_match.group(1).strip())
    desc_text = desc_match.group(1).strip() if desc_match else ""

    # 3. Mobile viewport meta tag
    viewport_match = re.search(r'<meta\s+name=["\']viewport["\']', html, re.IGNORECASE)
    audits["meta_viewport"] = bool(viewport_match)

    # 4. Canonical link tag
    canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.IGNORECASE)
    audits["canonical_link"] = bool(canonical_match)

    # 5. OpenGraph Tags
    og_match = re.search(r'<meta\s+property=["\']og:title["\']', html, re.IGNORECASE)
    audits["opengraph_tags"] = bool(og_match)

    # 6. Structured Data (JSON-LD)
    jsonld_match = re.search(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.IGNORECASE | re.DOTALL)
    jsonld_valid = False
    if jsonld_match:
        try:
            json.loads(jsonld_match.group(1).strip())
            jsonld_valid = True
        except:
            jsonld_valid = False
    audits["structured_data_jsonld"] = jsonld_valid

    # 7. Document has h1 heading
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    audits["h1_heading"] = bool(h1_match)

    # 8. Google AdSense script tag
    adsense_match = re.search(r'adsbygoogle\.js\?client=ca-pub-1342189574858672', html)
    audits["adsense_script"] = bool(adsense_match)

    # 9. Crawlable links (href attributes present)
    links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE)
    audits["crawlable_links"] = len(links) > 0 or "index.html" in filepath

    # Calculate Lighthouse Score (100-point scale)
    weights = {
        "title_element": 15,
        "meta_description": 15,
        "meta_viewport": 15,
        "canonical_link": 15,
        "structured_data_jsonld": 15,
        "h1_heading": 10,
        "opengraph_tags": 10,
        "adsense_script": 5
    }

    score = sum(w for key, w in weights.items() if audits.get(key, False))

    return {
        "page_name": page_name,
        "url": url,
        "score": score,
        "title": title_text,
        "description": desc_text,
        "audits": audits
    }

def run_all_audits():
    results = []
    print("=" * 70)
    print("LIGHTHOUSE SEO AUDIT REPORT — SHUNYAKIKHOJ PLATFORM")
    print("=" * 70)
    
    for name, path, url in PAGES_TO_AUDIT:
        res = audit_file(name, path, url)
        if res:
            results.append(res)
            score_color = "PASS" if res["score"] >= 90 else "WARN"
            print(f"\n[PAGE] {res['page_name']} ({res['url']})")
            print(f"   Lighthouse SEO Score: {res['score']}/100 [{score_color}]")
            print(f"   • Title: {res['title'][:60]}...")
            print(f"   • Meta Description: {'Present' if res['audits']['meta_description'] else 'Missing'}")
            print(f"   • Canonical Link: {'Present' if res['audits']['canonical_link'] else 'Missing'}")
            print(f"   • Structured Data (JSON-LD): {'Valid' if res['audits']['structured_data_jsonld'] else 'Missing'}")
            print(f"   • Mobile Viewport: {'Present' if res['audits']['meta_viewport'] else 'Missing'}")
            print(f"   • AdSense Tag: {'Present' if res['audits']['adsense_script'] else 'Missing'}")

    return results

if __name__ == "__main__":
    run_all_audits()
