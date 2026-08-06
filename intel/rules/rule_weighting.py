# -*- coding: utf-8 -*-
"""
rule_weighting.py
Deliverable 5: Rule Weighting Engine
Assigns continuous weighted potency scores based on rule priority, planet strength,
dasha applicability, and evidence reliability instead of binary boolean true/false.
"""

from typing import Dict, Any, List
from .rule_library import AstrologicalRule

class RuleWeightingEngine:
    """Calculates weighted continuous impact scores for rules."""

    @staticmethod
    def calculate_weighted_score(
        rule: AstrologicalRule,
        planet_shadbala_ratio: float = 1.0,
        is_dasha_active: bool = False,
        is_transit_active: bool = False
    ) -> Dict[str, Any]:

        base_weight = rule.weight
        conf = rule.confidence

        # Dynamic potency multipliers
        dasha_mult = 1.5 if is_dasha_active else 0.8
        transit_mult = 1.25 if is_transit_active else 0.9
        strength_mult = max(0.5, min(2.0, planet_shadbala_ratio))

        effective_potency = base_weight * dasha_mult * transit_mult * strength_mult * conf
        effective_score = round(effective_potency * 100.0, 2)

        return {
            "rule_id": rule.rule_id,
            "rule_name": rule.name,
            "base_weight": rule.weight,
            "confidence": rule.confidence,
            "effective_score": effective_score,
            "impact": "POSITIVE" if rule.positive_impact else "NEGATIVE",
            "multipliers": {
                "dasha_multiplier": dasha_mult,
                "transit_multiplier": transit_mult,
                "strength_multiplier": round(strength_mult, 2)
            }
        }
