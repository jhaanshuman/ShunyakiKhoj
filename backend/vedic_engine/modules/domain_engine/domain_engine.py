# -*- coding: utf-8 -*-
"""
Domain Engine v5.0.
Synthesizes data from all core & module calculation outputs into deterministic scores and insights
across ALL 27 Life Domains as required by the v5.0 specification.
"""

from typing import Dict, Any, List

class DomainEngine:
    """Universal 27 Life Domains Synthesis Engine."""

    DOMAINS_27 = {
        'personality': {'display': 'Personality & Self', 'houses': [1], 'planets': ['Sun', 'Mars', 'Jupiter']},
        'health': {'display': 'Health & Immunity', 'houses': [1, 6, 8], 'planets': ['Sun', 'Moon', 'Mars']},
        'education': {'display': 'Primary & Higher Education', 'houses': [4, 5, 9], 'planets': ['Mercury', 'Jupiter']},
        'intelligence': {'display': 'Intelligence & Creativity', 'houses': [5], 'planets': ['Jupiter', 'Mercury']},
        'career': {'display': 'Career & Profession', 'houses': [10, 2, 6, 11], 'planets': ['Sun', 'Saturn', 'Mercury']},
        'government': {'display': 'Government Service & Authority', 'houses': [10, 1, 9], 'planets': ['Sun', 'Mars']},
        'business': {'display': 'Business & Commerce', 'houses': [7, 11, 3], 'planets': ['Mercury', 'Venus']},
        'wealth': {'display': 'Wealth & Finance', 'houses': [2, 11, 5, 9], 'planets': ['Jupiter', 'Venus', 'Moon']},
        'investments': {'display': 'Investments & Speculation', 'houses': [5, 11], 'planets': ['Jupiter', 'Mercury']},
        'property': {'display': 'Property & Real Estate', 'houses': [4, 12], 'planets': ['Mars', 'Saturn', 'Venus']},
        'vehicles': {'display': 'Vehicles & Vahana', 'houses': [4], 'planets': ['Venus', 'Moon']},
        'marriage': {'display': 'Marriage & Partnerships', 'houses': [7, 2, 5], 'planets': ['Venus', 'Jupiter', 'Moon']},
        'relationships': {'display': 'Relationships & Social Circle', 'houses': [7, 11], 'planets': ['Venus', 'Mercury']},
        'children': {'display': 'Children & Progeny', 'houses': [5, 9], 'planets': ['Jupiter', 'Moon']},
        'parents': {'display': 'Parents & Ancestors', 'houses': [4, 9, 10], 'planets': ['Sun', 'Moon']},
        'siblings': {'display': 'Siblings & Courage', 'houses': [3, 11], 'planets': ['Mars', 'Mercury']},
        'foreign': {'display': 'Foreign Travel & Relocation', 'houses': [12, 9, 3], 'planets': ['Rahu', 'Saturn']},
        'spirituality': {'display': 'Spirituality & Liberation', 'houses': [9, 12, 5, 4], 'planets': ['Jupiter', 'Ketu']},
        'fame': {'display': 'Fame & Recognition', 'houses': [10, 11, 1], 'planets': ['Sun', 'Jupiter']},
        'leadership': {'display': 'Leadership & Command', 'houses': [1, 10], 'planets': ['Sun', 'Mars']},
        'litigation': {'display': 'Litigation & Enemies', 'houses': [6, 8], 'planets': ['Mars', 'Rahu', 'Saturn']},
        'accidents': {'display': 'Accidents & Sudden Hazards', 'houses': [8, 6, 12], 'planets': ['Mars', 'Rahu', 'Ketu']},
        'longevity': {'display': 'Longevity & Lifespan', 'houses': [8, 1, 3], 'planets': ['Saturn', 'Jupiter']},
        'retirement': {'display': 'Retirement & Late Life', 'houses': [12, 4], 'planets': ['Saturn', 'Jupiter']},
        'charity': {'display': 'Charity & Karma Yoga', 'houses': [9, 12], 'planets': ['Jupiter', 'Ketu']},
        'mental_wellbeing': {'display': 'Mental Wellbeing & Peace', 'houses': [1, 4, 5], 'planets': ['Moon', 'Jupiter']},
        'hidden_assets': {'display': 'Inheritance & Hidden Assets', 'houses': [8], 'planets': ['Jupiter', 'Saturn', 'Mars']}
    }

    @classmethod
    def synthesize_27_domains(cls, master_obj: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Synthesizes all 27 domains into normalized scores, summaries, and supporting factors."""
        domains_result = []

        house_analysis = master_obj.get('house_analysis', {})
        planet_state = master_obj.get('planet_state', {})
        rule_matches = master_obj.get('rule_matches', [])
        all_yogas = master_obj.get('all_yogas', master_obj.get('yogas', []))
        event_indicators = master_obj.get('event_indicators', {})
        timeline = master_obj.get('timeline', {})

        # Group rules by domain
        rules_by_domain = {}
        for rule in rule_matches:
            d_name = str(rule.get('domain', '')).lower()
            rules_by_domain.setdefault(d_name, []).append(rule)

        for domain_key, meta in cls.DOMAINS_27.items():
            primary_houses = meta['houses']
            primary_planets = meta['planets']

            # House scores average
            h_scores = [house_analysis.get(f'house_{h}', {}).get('house_score', 50.0) for h in primary_houses]
            house_avg = sum(h_scores) / max(len(h_scores), 1)

            # Planet strengths average
            p_strengths = [planet_state.get(p, {}).get('overall_strength', 50.0) for p in primary_planets]
            planet_avg = sum(p_strengths) / max(len(p_strengths), 1)

            # Event indicator score if present
            event_score = event_indicators.get(domain_key, 50.0)

            # Matching rules
            domain_rules = rules_by_domain.get(domain_key, [])
            rule_avg_conf = sum(r.get('confidence', 50) for r in domain_rules) / max(len(domain_rules), 1) if domain_rules else 50.0

            # Composite Score (0-100)
            composite_score = round(
                house_avg * 0.35 +
                planet_avg * 0.25 +
                event_score * 0.25 +
                rule_avg_conf * 0.15,
                1
            )
            composite_score = min(100.0, max(0.0, composite_score))

            # Quality classification
            if composite_score >= 75.0:
                quality = "Exceptionally Strong"
            elif composite_score >= 60.0:
                quality = "Favorable"
            elif composite_score >= 45.0:
                quality = "Moderate"
            elif composite_score >= 30.0:
                quality = "Challenging"
            else:
                quality = "Afflicted"

            # Filter relevant yogas
            supporting_yogas = [
                y.get('name', '') for y in all_yogas
                if any(domain_key in str(aff).lower() for aff in y.get('affected_domains', [])) or
                   any(domain_key in str(y.get('category', '')).lower() for kw in [domain_key])
            ][:5]

            domains_result.append({
                "domain": domain_key,
                "domain_key": domain_key,
                "domain_display": meta['display'],
                "display_name": meta['display'],
                "domain_score": composite_score,
                "quality_label": quality,
                "confidence": round(rule_avg_conf, 1),
                "primary_houses": primary_houses,
                "primary_planets": primary_planets,
                "house_avg_score": round(house_avg, 1),
                "planet_avg_strength": round(planet_avg, 1),
                "matching_rules_count": len(domain_rules),
                "supporting_yogas": supporting_yogas,
                "summary": domain_rules[0].get('description', f"Indications for {meta['display']}.") if domain_rules else f"Standard placements for {meta['display']}.",
                "top_rule_summary": domain_rules[0].get('description', f"Indications for {meta['display']}.") if domain_rules else f"Standard placements for {meta['display']}."
            })

        return sorted(domains_result, key=lambda x: x['domain_score'], reverse=True)
