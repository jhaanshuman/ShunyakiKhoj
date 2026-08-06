# -*- coding: utf-8 -*-
"""
generate_10k_scenarios.py
Generates 10,000 structured life scenarios across 50 primary life domains.
Saves output to webpage/features_db.json for the PhalDeepika Web Intelligence Portal.
"""

import json
import os

DOMAINS_DEFINITION = [
    ("CAREER", "Career & Profession", "💼"),
    ("MARRIAGE", "Marriage & Relationships", "💍"),
    ("CHILDREN", "Children & Parenthood", "👶"),
    ("WEALTH", "Finance, Stock Trading & Wealth", "💰"),
    ("FOREIGN", "Foreign Travel, Visa & PR", "✈️"),
    ("HEALTH", "Health, Vitality & Longevity", "🩺"),
    ("PROPERTY", "Real Estate & Housing Assets", "🏰"),
    ("VEHICLES", "Luxury Vehicles & Automobiles", "🚘"),
    ("LEGAL", "Litigation, Disputes & Court", "⚖️"),
    ("EDUCATION", "Academics & Competitive Exams", "🎓"),
    ("SPIRITUALITY", "Spiritual Growth & Moksha", "🪔"),
    ("BUSINESS", "Entrepreneurship & Startups", "🏬"),
    ("TECHNOLOGY", "AI, Coding & Tech Careers", "💻"),
    ("CIVIL_SERVICES", "IAS, IPS & Government Posts", "🏛️"),
    ("SPORTS", "Athletics & Competitive Sports", "⚽"),
    ("ARTS_CINEMA", "Arts, Film & Acting Fame", "🎬"),
    ("POLITICS", "Political Power & Leadership", "👑"),
    ("AGRICULTURE", "Farming, Land & Agri-Business", "🌾"),
    ("SOCIAL_STATUS", "Fame, Reputation & Honors", "🌟"),
    ("FAMILY", "Ancestral Relations & In-laws", "👨‍👩‍👧‍👦"),
    ("MENTAL_HEALTH", "Psychological Well-being & Peace", "🧠"),
    ("LONGEVITY", "Lifespan & Longevity Indicators", "⏳"),
    ("INLAWS", "Spousal Family & In-law Relations", "🤝"),
    ("PETS_ANIMALS", "Pets, Livestock & Animal Care", "🐕"),
    ("SPECULATION", "Lottery, Crypto & Day Trading", "📈"),
    ("FREELANCING", "Gig Economy & Remote Work", "🎧"),
    ("HIGHER_LEARNING", "PhD, Research & Academics", "📚"),
    ("PUBLIC_FAME", "National & International Awards", "🏆"),
    ("HOUSING", "Home Construction & Renovation", "🏡"),
    ("INHERITANCE", "Wills, Ancestral Property & Heirs", "📜"),
    ("LOANS_DEBT", "Banking Loans & Debt Recovery", "🏦"),
    ("PARTNERSHIPS", "Business Alliances & Deals", "🤝"),
    ("ENEMIES", "Competitors & Secret Enemies", "🛡️"),
    ("YOGA_SIDDHI", "Kundalini & Tantric Sadhana", "🧘"),
    ("OCCULT", "Astrology, Tarot & Occult Studies", "🔮"),
    ("MEDIA", "Influencer, YouTube & Social Media", "📱"),
    ("GAMING", "Esports, Streaming & Gaming", "🎮"),
    ("FUNDING", "Venture Capital & Seed Grants", "💸"),
    ("GOVT_TENDERS", "Public Contracts & Subsidies", "📜"),
    ("FOREIGN_EDU", "Study Abroad & Scholarships", "🌍"),
    ("SURGERY", "Medical Operations & Recovery", "🏥"),
    ("ACCIDENTS", "Travel Safety & Physical Protection", "⚠️"),
    ("GURUS", "Spiritual Mentors & Diksha", "🕉️"),
    ("CHARITY", "Philanthropy & Social Service", "🤲"),
    ("LAND_DISPUTES", "Boundary Disputes & Titles", "🗺️"),
    ("ELDER_CARE", "Parents' Health & Caregiving", "👴"),
    ("SIBLINGS", "Brother & Sister Relations", "👫"),
    ("CONSPIRACY", "Workplace Plotting & Defamation", "🔍"),
    ("INSURANCE", "Insurance Claims & Settlements", "📋"),
    ("RETIREMENT", "Pension & Post-Retirement Life", "🌅")
]

SCENARIO_TEMPLATES = [
    "Will I achieve major success in {domain_name} during my active Dasha?",
    "When is the most favorable timing for {domain_name} in 2026-2028?",
    "What classical planetary yogas govern my {domain_name} promise?",
    "Will transiting Jupiter bring significant breakthroughs in {domain_name}?",
    "Are there malefic Saturn or Rahu delays affecting my {domain_name}?",
    "What remedies enhance 1st lord and Karaka strength for {domain_name}?",
    "How does the Divisional Varga chart influence my {domain_name} trajectory?",
    "Will I overcome unexpected obstacles in {domain_name} this year?",
    "What is the exact Ashtakvarga SAV bindu strength for my {domain_name} house?",
    "Will my active Antardasha unlock financial and personal growth in {domain_name}?",
    "How does 10th and 9th lord aspect impact my {domain_name} decisions?",
    "Will I face legal or administrative delays in {domain_name}?",
    "What is the ultimate peak potential for {domain_name} in my natal chart?",
    "Is long-distance movement or relocation indicated for {domain_name}?",
    "Will my family and mentors support my growth in {domain_name}?",
    "What KP sublord significators rule my {domain_name} prospects?",
    "Will sudden luck or inheritance boost my {domain_name} scenario?",
    "How to neutralize afflictions in the 4th, 5th, 7th, 9th, or 10th houses for {domain_name}?",
    "When will my pending decisions in {domain_name} reach final closure?",
    "What classical text citations from BPHS and Phaladeepika validate my {domain_name}?"
]

def generate_10k_db():
    domains_data = []
    total_count = 0

    for domain_id, domain_name, icon in DOMAINS_DEFINITION:
        features = []
        for i in range(1, 201): # 200 features per domain * 50 domains = 10,000 features
            template = SCENARIO_TEMPLATES[(i - 1) % len(SCENARIO_TEMPLATES)]
            scenario_name = f"{domain_name} Scenario #{i}: " + template.format(domain_name=domain_name)
            feat_id = f"{domain_id}_{i:03d}"
            features.append({
                "id": feat_id,
                "name": scenario_name,
                "query": scenario_name
            })
            total_count += 1

        domains_data.append({
            "category_id": domain_id,
            "category_name": domain_name,
            "icon": icon,
            "features": features
        })

    db_object = {
        "total_features": total_count,
        "domains_count": len(domains_data),
        "domains": domains_data
    }

    output_path = os.path.join("webpage", "features_db.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(db_object, f, indent=2)

    print(f"Successfully generated {total_count} scenarios across {len(domains_data)} domains in {output_path}!")

if __name__ == "__main__":
    generate_10k_db()
