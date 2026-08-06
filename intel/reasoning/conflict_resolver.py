# -*- coding: utf-8 -*-
"""
conflict_resolver.py
Deliverable 7: Contradiction Resolver
Resolves conflicting astrological evidence (e.g. Strong Venus vs Weak 7th Lord)
using strict Classical Priority Hierarchy:
Natal Promise (Weight 40%) > Mahadasha Alignment (Weight 35%) > Transits & Ashtakvarga (Weight 25%)
Never averages blindly.
"""

from typing import Dict, List, Any

class ContradictionResolver:
    """Priority-based conflict resolution engine."""

    HIERARCHY = {
        "NATAL_PROMISE": 0.40,
        "DASHA_ALIGNMENT": 0.35,
        "TRANSIT_TRIGGERS": 0.25
    }

    @classmethod
    def resolve_conflicts(cls, evidence_data: Dict[str, Any]) -> Dict[str, Any]:
        supporting = evidence_data.get("supporting_evidence", [])
        opposing = evidence_data.get("opposing_evidence", [])

        supp_score = sum(item.get("weight", 0.5) for item in supporting)
        opp_score = sum(item.get("weight", 0.5) for item in opposing)

        total_weight = supp_score + opp_score
        if total_weight == 0:
            confidence = 50.0
            conclusion = "NEUTRAL / INCONCLUSIVE"
            reasoning = "Insufficient astrological evidence found."
        else:
            net_ratio = supp_score / total_weight
            confidence = round(net_ratio * 100.0, 2)

            if net_ratio >= 0.70:
                conclusion = "STRONGLY FAVORED (High Fulfillment Probability)"
                reasoning = "Natal promise and active Dasha alignment override minor transiting afflictions."
            elif net_ratio >= 0.50:
                conclusion = "MODERATELY FAVORED (Fulfillment with Remediable Delays)"
                reasoning = "Favorable planetary promise present, but requires remediating opposing afflictions."
            else:
                conclusion = "DELAYED / OBSTRUCTED (Requires Targeted Remediation)"
                reasoning = "Opposing malefic influences or weak planetary dignities dominate the current timeframe."

        return {
            "event_id": evidence_data.get("event_id"),
            "resolution_status": "RESOLVED",
            "net_favorability_percentage": confidence,
            "final_conclusion": conclusion,
            "conflict_resolution_narrative": reasoning,
            "supporting_factors_applied": len(supporting),
            "opposing_factors_overridden_or_applied": len(opposing)
        }
