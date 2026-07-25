# -*- coding: utf-8 -*-
"""
Domain Synthesis Engine v1.0.
Synthesizes data from all sub-engines into domain-level predictions.
Each domain (career, marriage, wealth, etc.) gets a SINGLE consolidated object.
"""

class DomainSynthesisEngine:
    DOMAINS = [
        'career', 'marriage', 'wealth', 'education', 'children', 'health',
        'property', 'siblings', 'parents', 'foreign', 'spirituality',
        'litigation', 'business', 'government', 'fame', 'longevity', 'accidents'
    ]

    DOMAIN_DISPLAY = {
        'career': 'Career & Profession', 'marriage': 'Marriage & Partnerships',
        'wealth': 'Wealth & Finance', 'education': 'Education & Intellect',
        'children': 'Children & Progeny', 'health': 'Health & Vitality',
        'property': 'Property & Real Estate', 'siblings': 'Siblings & Courage',
        'parents': 'Parents & Ancestors', 'foreign': 'Foreign Travel & Relocation',
        'spirituality': 'Spirituality & Liberation', 'litigation': 'Litigation & Enemies',
        'business': 'Business & Commerce', 'government': 'Government & Authority',
        'fame': 'Fame & Recognition', 'longevity': 'Longevity & Life Span',
        'accidents': 'Accidents & Sudden Events'
    }

    DOMAIN_RULE_MAP = {
        'career': 'Career', 'marriage': 'Marriage', 'wealth': 'Wealth',
        'education': 'Education', 'children': 'Children', 'health': 'Health',
        'property': 'Property', 'siblings': 'Siblings', 'parents': 'Parents',
        'foreign': 'Foreign Travel', 'spirituality': 'Spirituality',
        'litigation': 'Litigation', 'business': 'Business',
        'government': 'Government', 'fame': 'Fame',
        'longevity': 'Longevity', 'accidents': 'Accidents'
    }

    DOMAIN_PRIMARY_HOUSES = {
        'career': [10, 2, 6, 11], 'marriage': [7, 2, 5], 'wealth': [2, 11, 5, 9],
        'education': [5, 4, 9], 'children': [5, 9], 'health': [1, 6, 8],
        'property': [4, 12], 'siblings': [3, 11], 'parents': [4, 9, 10],
        'foreign': [12, 9, 3], 'spirituality': [9, 12, 5, 4],
        'litigation': [6, 8], 'business': [7, 11, 3],
        'government': [10, 1, 9], 'fame': [10, 11],
        'longevity': [8, 1, 3], 'accidents': [8, 6, 12]
    }

    DOMAIN_PRIMARY_PLANETS = {
        'career': ['Sun', 'Saturn', 'Mercury'],
        'marriage': ['Venus', 'Jupiter', 'Moon'],
        'wealth': ['Jupiter', 'Venus', 'Moon'],
        'education': ['Mercury', 'Jupiter'],
        'children': ['Jupiter', 'Moon'],
        'health': ['Sun', 'Moon', 'Mars'],
        'property': ['Mars', 'Venus', 'Moon'],
        'siblings': ['Mars', 'Mercury'],
        'parents': ['Sun', 'Moon'],
        'foreign': ['Rahu', 'Saturn'],
        'spirituality': ['Jupiter', 'Ketu'],
        'litigation': ['Mars', 'Rahu', 'Saturn'],
        'business': ['Mercury', 'Venus'],
        'government': ['Sun', 'Mars'],
        'fame': ['Sun', 'Jupiter'],
        'longevity': ['Saturn', 'Jupiter'],
        'accidents': ['Mars', 'Rahu', 'Ketu']
    }

    @staticmethod
    def synthesize(master_obj: dict) -> list:
        synth = []
        rule_matches = master_obj.get('rule_matches', [])
        event_indicators = master_obj.get('event_indicators', {})
        house_analysis = master_obj.get('house_analysis', {})
        planet_state = master_obj.get('planet_state', {})
        evidence = master_obj.get('evidence_registry', {})
        yogas = master_obj.get('yogas', [])
        advanced_yogas = master_obj.get('advanced_yogas', [])
        dasha = master_obj.get('dasha', {})
        vimshottari = dasha.get('vimshottari', [])

        all_yogas = list(yogas) + list(advanced_yogas)

        # Group rules by domain
        rules_by_domain = {}
        for rule in rule_matches:
            rules_by_domain.setdefault(rule.get('domain', ''), []).append(rule)

        # Current dasha
        current_md = vimshottari[0] if vimshottari else {}
        current_md_lord = current_md.get('lord', '')
        antardashas = current_md.get('antardashas', [])
        current_ad_lord = antardashas[0].get('lord', '') if antardashas else ''
        current_dasha_str = f"{current_md_lord} MD / {current_ad_lord} AD" if current_ad_lord else current_md_lord

        for domain_key in DomainSynthesisEngine.DOMAINS:
            rule_domain = DomainSynthesisEngine.DOMAIN_RULE_MAP.get(domain_key, '')
            domain_rules = rules_by_domain.get(rule_domain, [])
            domain_evidence = evidence.get(rule_domain, {})

            if not domain_rules:
                continue

            primary_houses = DomainSynthesisEngine.DOMAIN_PRIMARY_HOUSES.get(domain_key, [])
            primary_planets = DomainSynthesisEngine.DOMAIN_PRIMARY_PLANETS.get(domain_key, [])

            # House scores for primary houses
            house_scores = {}
            for h in primary_houses:
                score = house_analysis.get(f'house_{h}', {}).get('house_score', 50.0)
                house_scores[h] = round(score, 1)

            # Planet strengths for primary planets
            planet_strengths = {}
            for p in primary_planets:
                state = planet_state.get(p, {})
                planet_strengths[p] = state.get('overall_strength', 50.0)

            # Composite strength score
            house_avg = sum(house_scores.values()) / len(house_scores) if house_scores else 50
            planet_avg = sum(planet_strengths.values()) / len(planet_strengths) if planet_strengths else 50
            event_score = event_indicators.get(domain_key, 50.0)

            # Rule confidence average
            rule_avg_conf = sum(r.get('confidence', 50) for r in domain_rules) / max(len(domain_rules), 1)

            # Composite domain score
            domain_score = round(house_avg * 0.35 + planet_avg * 0.25 + event_score * 0.25 + rule_avg_conf * 0.15, 1)

            # Supporting yogas for this domain
            domain_yogas = [
                y.get('name', '') for y in all_yogas
                if any(kw in (y.get('category', '') + y.get('name', ''))
                       for kw in [rule_domain, 'Raja', 'Dhana', 'Mahapurusha'])
            ]

            # Conflicting factors
            conflicts = []
            for rule in domain_rules:
                conflicts.extend(rule.get('conflicting_factors', []))
            conflicts = list(set(conflicts))

            # Dasha planet state for relevance
            md_state = planet_state.get(current_md_lord, {})
            md_in_primary = current_md_lord in primary_planets
            ad_in_primary = current_ad_lord in primary_planets
            dasha_activated = md_in_primary or ad_in_primary

            # Prediction summary
            top_rule = max(domain_rules, key=lambda r: r.get('confidence', 0), default={})
            summary = top_rule.get('description', f'Moderate {rule_domain} indications.')

            synth.append({
                "domain": domain_key,
                "domain_display": DomainSynthesisEngine.DOMAIN_DISPLAY.get(domain_key, domain_key),
                "domain_score": min(100, domain_score),
                "confidence": round(rule_avg_conf, 1),
                "summary": summary,
                "house_scores": house_scores,
                "planet_strengths": planet_strengths,
                "supporting_rules": [r.get('id', '') for r in domain_rules],
                "supporting_yogas": domain_yogas[:5],
                "conflicting_factors": conflicts,
                "rule_count": len(domain_rules),
                "yoga_count": len(domain_yogas),
                "current_dasha": current_dasha_str,
                "dasha_activated": dasha_activated,
                "evidence_id": domain_evidence.get('evidence_id', ''),
                "event_indicator_score": round(event_score, 1)
            })

        return sorted(synth, key=lambda x: x['domain_score'], reverse=True)
