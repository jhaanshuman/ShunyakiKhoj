# -*- coding: utf-8 -*-
"""
Structured Event Indicator Engine.
Synthesizes matched deterministic rules and house scores into normalized domain indicators (0-100).
"""

class EventIndicatorEngine:
    @staticmethod
    def calculate_event_indicators(master_obj: dict) -> dict:
        rule_matches = master_obj.get('rule_matches', [])
        houses_analysis = master_obj.get('house_analysis', {})

        domains = {
            "career": 10,
            "marriage": 7,
            "wealth": 11,
            "education": 5,
            "children": 5,
            "health": 1,
            "property": 4,
            "business": 7,
            "government": 10,
            "spirituality": 9
        }

        indicators = {}

        for dom, house_num in domains.items():
            # Base house score
            h_key = f"house_{house_num}"
            base_score = houses_analysis.get(h_key, {}).get('house_score', 50.0)

            # Rule match boost
            rule_score = 0.0
            rule_count = 0
            for r in rule_matches:
                if r.get('domain', '').lower() == dom:
                    rule_score += r.get('strength', 50.0)
                    rule_count += 1

            if rule_count > 0:
                avg_rule_score = rule_score / rule_count
                final_score = round((base_score * 0.4) + (avg_rule_score * 0.6), 2)
            else:
                final_score = round(base_score, 2)

            indicators[dom] = min(100.0, max(10.0, final_score))

        return indicators
