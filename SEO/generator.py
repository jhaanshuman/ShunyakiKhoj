# -*- coding: utf-8 -*-
"""
ShunyakiKhoj Automated SEO Page, Schema & Sitemap Generator v1.0
Generates clean, crawlable static HTML landing pages, JSON-LD schemas,
comprehensive sitemap.xml, and updated robots.txt.
"""

import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEO_DIR = os.path.join(ROOT_DIR, "SEO")
MANIFEST_PATH = os.path.join(SEO_DIR, "seo_manifest.json")
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")
ROBOTS_PATH = os.path.join(ROOT_DIR, "robots.txt")

DOMAIN = "https://shunyakikhoj.co.in"
ADSENSE_CODE = '<meta name="google-adsense-account" content="ca-pub-1342189574858672">\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1342189574858672" crossorigin="anonymous"></script>'

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — ShunyakiKhoj Vedic Astrology & Sanskrit AI</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords_str}">
<link rel="canonical" href="{canonical_url}">

<!-- OpenGraph & Twitter -->
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical_url}">
<meta property="og:image" content="{domain}/logo.png">
<meta name="twitter:card" content="summary_large_image">

{adsense_code}

<link rel="stylesheet" href="/style.css">
<style>
.seo-landing-wrapper {{
    max-width: 1050px;
    margin: 40px auto;
    padding: 30px;
    background: rgba(15, 23, 42, 0.95);
    border-radius: 16px;
    border: 1px solid #334155;
    color: #f8fafc;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}
.seo-title {{
    font-size: 2.2rem;
    font-weight: 800;
    color: #fbbf24;
    margin-bottom: 15px;
    border-bottom: 2px solid #334155;
    padding-bottom: 12px;
}}
.seo-subtitle {{
    font-size: 1.1rem;
    color: #cbd5e1;
    line-height: 1.6;
    margin-bottom: 25px;
}}
.seo-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin: 30px 0;
}}
.seo-card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 20px;
}}
.seo-card h3 {{
    color: #4ade80;
    margin-top: 0;
    font-size: 1.15rem;
}}
.btn-cta {{
    display: inline-block;
    background: linear-gradient(135deg, #a23922 0%, #fc8c10 100%);
    color: #ffffff;
    font-weight: 800;
    padding: 14px 28px;
    border-radius: 30px;
    text-decoration: none;
    font-size: 1.05rem;
    margin-top: 20px;
    transition: transform 0.2s;
}}
.btn-cta:hover {{
    transform: translateY(-2px);
}}
.keywords-chip-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 20px;
}}
.keyword-chip {{
    background: rgba(251, 191, 36, 0.12);
    border: 1px solid rgba(251, 191, 36, 0.3);
    color: #fbbf24;
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 0.8rem;
    font-weight: 600;
}}
</style>

<!-- JSON-LD Structured Data Schema -->
<script type="application/ld+json">
{json_ld_schema}
</script>
</head>
<body>

<div class="seo-landing-wrapper">
    <h1 class="seo-title">{title}</h1>
    <p class="seo-subtitle">{description}</p>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="{cta_link}" class="btn-cta">🔮 Launch Live {name} Calculator</a>
    </div>

    <div class="seo-grid">
        <div class="seo-card">
            <h3>⚡ High-Precision Engine</h3>
            <p>Calculated using Swiss Ephemeris & Drik Ganita astronomical observation algorithms. Delivers 100% accurate planetary longitudes, divisional charts (D1 to D144), and traditional Vedic time cycles.</p>
        </div>
        <div class="seo-card">
            <h3>📜 Classical Text Rules</h3>
            <p>Integrated with Brihat Parasara Hora Sastra (BPHS), Jaimini Sutras, Phaladeepika, and Saravali for comprehensive yoga evaluation and planetary strength assessment (Shadbala & Ashtakavarga).</p>
        </div>
        <div class="seo-card">
            <h3>🌐 Multilingual & AI Assisted</h3>
            <p>Supports English, Hindi, and original Devanagari Sanskrit terminology with embedded AI context synthesis for personalized astrological and spiritual insights.</p>
        </div>
    </div>

    <h2 style="color: #fbbf24; margin-top: 40px; border-bottom: 1px solid #334155; padding-bottom: 8px;">Targeted Research Topics ({keywords_count}+ Keywords)</h2>
    <div class="keywords-chip-container">
        {keywords_chips}
    </div>

    <div style="margin-top: 50px; text-align: center; border-top: 1px solid #334155; padding-top: 20px; color: #94a3b8; font-size: 0.85rem;">
        <p>© 2026 ShunyakiKhoj | <a href="{domain}" style="color: #fbbf24; text-decoration: none;">shunyakikhoj.co.in</a> — Universal Vedic Astrology Engine v5.3</p>
    </div>
</div>

</body>
</html>
"""

def generate_seo_system():
    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: Manifest path {MANIFEST_PATH} not found.")
        return

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    categories = manifest.get("categories", [])
    sitemap_urls = [
        {"loc": DOMAIN, "priority": "1.0", "changefreq": "daily"},
        {"loc": f"{DOMAIN}/index.html", "priority": "1.0", "changefreq": "daily"},
        {"loc": f"{DOMAIN}/jyotish_window.html", "priority": "0.9", "changefreq": "daily"}
    ]

    for cat in categories:
        slug = cat["slug"]
        name = cat["name"]
        cat_dir = os.path.join(ROOT_DIR, slug)
        os.makedirs(cat_dir, exist_ok=True)
        
        index_file = os.path.join(cat_dir, "index.html")
        canonical_url = f"{DOMAIN}/{slug}/"
        cta_link = f"{DOMAIN}/index.html?tab={cat['id']}"
        
        title = f"Free {name} — Accurate Vedic Astrology & Calculations"
        description = f"Explore free online {name}. Powered by Swiss Ephemeris & classical Jyotish rules for accurate astronomical calculations, charts, and predictions."
        
        keywords_list = cat.get("head_keywords", [])
        keywords_str = ", ".join(keywords_list)
        keywords_chips = "".join([f'<span class="keyword-chip">{kw}</span>' for kw in keywords_list])
        
        # Build JSON-LD Schema
        schema_dict = {
            "@context": "https://schema.org",
            "@type": cat.get("schema", "WebApplication"),
            "name": name,
            "url": canonical_url,
            "description": description,
            "applicationCategory": "AstrologyApplication",
            "operatingSystem": "All",
            "author": {
                "@type": "Organization",
                "name": "ShunyakiKhoj",
                "url": DOMAIN
            }
        }
        json_ld_schema = json.dumps(schema_dict, indent=2)

        page_html = PAGE_TEMPLATE.format(
            title=title,
            description=description,
            keywords_str=keywords_str,
            canonical_url=canonical_url,
            domain=DOMAIN,
            adsense_code=ADSENSE_CODE,
            json_ld_schema=json_ld_schema,
            name=name,
            cta_link=cta_link,
            keywords_count=cat.get("keywords_count", 500),
            keywords_chips=keywords_chips
        )

        with open(index_file, "w", encoding="utf-8") as out_f:
            out_f.write(page_html)

        print(f"Generated SEO Landing Page: /{slug}/index.html")

        sitemap_urls.append({
            "loc": canonical_url,
            "priority": str(cat.get("priority", 0.8)),
            "changefreq": cat.get("changefreq", "weekly")
        })

    # Build XML Sitemap
    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    
    for item in sitemap_urls:
        sitemap_xml.append("  <url>")
        sitemap_xml.append(f"    <loc>{item['loc']}</loc>")
        sitemap_xml.append(f"    <changefreq>{item['changefreq']}</changefreq>")
        sitemap_xml.append(f"    <priority>{item['priority']}</priority>")
        sitemap_xml.append("  </url>")
    
    sitemap_xml.append("</urlset>")

    with open(SITEMAP_PATH, "w", encoding="utf-8") as sm_f:
        sm_f.write("\n".join(sitemap_xml))
    print(f"Generated master sitemap.xml with {len(sitemap_urls)} URLs.")

    # Update robots.txt
    robots_content = f"""User-agent: *
Allow: /
Disallow: /api/

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(ROBOTS_PATH, "w", encoding="utf-8") as rb_f:
        rb_f.write(robots_content)
    print("Updated robots.txt with sitemap directive.")

if __name__ == "__main__":
    generate_seo_system()
