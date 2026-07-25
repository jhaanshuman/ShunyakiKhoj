# -*- coding: utf-8 -*-
"""
Evidence Engine v1.0.
Compiles a complete evidence registry for all predictions.
Every prediction carries verifiable, traceable evidence.
"""

class EvidenceEngine:
    DOMAIN_LIFE_AREA_MAP = {
        'Career': 'career', 'Marriage': 'marriage', 'Wealth': 'wealth',
        'Education': 'education', 'Children': 'children', 'Health': 'health',
        'Property': 'property', 'Siblings': 'siblings', 'Parents': 'parents',
        'Foreign Travel': 'foreign', 'Spirituality': 'spirituality',
        'Litigation': 'litigation', 'Business': 'business',
        'Government': 'government', 'Fame': 'fame',
        'Longevity': 'longevity', 'Accidents': 'accidents'
    }

    @staticmethod
    def compile(master_obj: dict) -> dict:
        evidence_registry = {}
        rule_matches = master_obj.get('rule_matches', [])
        advanced_yogas = master_obj.get('advanced_yogas', [])
        yogas = master_obj.get('yogas', [])
        event_indicators = master_obj.get('event_indicators', {})
        planet_state = master_obj.get('planet_state', {})
        house_analysis = master_obj.get('house_analysis', {})
        dasha = master_obj.get('dasha', {})
        vimshottari = dasha.get('vimshottari', [])
        transits = master_obj.get('transits', {})
        shadbala = master_obj.get('shadbala', {})
        dignities = master_obj.get('dignity', {})

        # Group rules by domain
        rules_by_domain = {}
        for rule in rule_matches:
            domain = rule.get('domain', 'General')
            rules_by_domain.setdefault(domain, []).append(rule)

        # Group yogas by domain (using category as proxy)
        all_yogas = list(yogas) + list(advanced_yogas)
        yoga_by_domain = {}
        for y in all_yogas:
            cat = y.get('category', '')
            name = y.get('name', '')
            if 'Career' in cat or 'Raja' in cat or 'Mahapurusha' in cat:
                yoga_by_domain.setdefault('Career', []).append(name)
            if 'Dhana' in cat or 'Wealth' in cat or 'Lakshmi' in cat:
                yoga_by_domain.setdefault('Wealth', []).append(name)
            if 'Marriage' in cat or 'Kalatra' in cat:
                yoga_by_domain.setdefault('Marriage', []).append(name)
            if 'Intellect' in cat or 'Education' in cat:
                yoga_by_domain.setdefault('Education', []).append(name)
            if 'Spiritual' in cat or 'Moksha' in cat:
                yoga_by_domain.setdefault('Spirituality', []).append(name)
            if 'Dosha' in cat:
                yoga_by_domain.setdefault('Doshas', []).append(name)

        # Current dasha info
        current_md = vimshottari[0] if vimshottari else {}
        current_md_lord = current_md.get('lord', '')
        antardashas = current_md.get('antardashas', [])
        current_ad_lord = antardashas[0].get('lord', '') if antardashas else ''

        for domain, life_key in EvidenceEngine.DOMAIN_LIFE_AREA_MAP.items():
            domain_rules = rules_by_domain.get(domain, [])
            if not domain_rules:
                continue

            # Sort rules by confidence
            domain_rules_sorted = sorted(domain_rules, key=lambda r: r.get('confidence', 0), reverse=True)
            best_rule = domain_rules_sorted[0]

            # Gather evidence chain from all rules
            all_evidence = []
            for rule in domain_rules_sorted:
                all_evidence.extend(rule.get('evidence_chain', []))
                all_evidence.extend(rule.get('matched_conditions', []))
            # Deduplicate
            seen = set()
            unique_evidence = []
            for e in all_evidence:
                if str(e) not in seen:
                    seen.add(str(e))
                    unique_evidence.append(e)

            # Gather conflicts
            all_conflicts = []
            for rule in domain_rules_sorted:
                all_conflicts.extend(rule.get('conflicting_factors', []))

            # All supporting rules
            supporting_rule_ids = [r.get('id', '') for r in domain_rules_sorted]

            # Supporting yogas for this domain
            supporting_yogas = list(set(yoga_by_domain.get(domain, [])))

            # Dasha relevance
            md_planet_state = planet_state.get(current_md_lord, {})
            dasha_relevance = "Strong" if md_planet_state.get('overall_strength', 50) >= 65 else "Moderate"

            # Domain score
            domain_score = round(event_indicators.get(life_key, 50.0), 1)

            # Net confidence (average of all rule confidences)
            avg_confidence = round(sum(r.get('confidence', 50) for r in domain_rules) / max(len(domain_rules), 1), 1)

            evidence_id = f"{domain.upper().replace(' ', '_')[:6]}_{len(domain_rules):03d}"

            evidence_registry[domain] = {
                "evidence_id": evidence_id,
                "domain": domain,
                "domain_score": domain_score,
                "confidence": avg_confidence,
                "evidence": unique_evidence[:10],  # Top 10 most relevant evidence items
                "conflicting_factors": list(set(all_conflicts)),
                "source_rules": supporting_rule_ids,
                "source_yogas": supporting_yogas,
                "current_dasha": f"{current_md_lord} MD {'/ ' + current_ad_lord + ' AD' if current_ad_lord else ''}",
                "dasha_relevance": dasha_relevance,
                "depends_on": ["house_analysis", "planet_state", "shadbala", "dignity", "rule_matches"],
                "generated_by": "EvidenceEngine v1.0"
            }

        return evidence_registry
