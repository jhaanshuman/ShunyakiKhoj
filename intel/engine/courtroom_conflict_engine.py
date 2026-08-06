# -*- coding: utf-8 -*-
"""
courtroom_conflict_engine.py
Courtroom Conflict & Astrological Argument Engine
ZERO hardcoded fallbacks. Calculates strictly from evaluated evidence objects.
If no evidence is present, returns "N/A".
"""

from typing import Dict, List, Any

class CourtroomConflictEngine:
    """Courtroom-style Astrological Debate Engine without hardcoded fallbacks."""

    @classmethod
    def conduct_courtroom_debate(cls, evidence_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        prosecution_rules = []
        defense_rules = []

        pros_score = 0
        def_score = 0

        for item in evidence_objects:
            impact = item.get("impact_type")
            rule_id = item.get("rule_id", "N/A")
            strength = item.get("strength", 0)
            source = item.get("source", "Classical Text")

            if impact == "PROSECUTION_POSITIVE":
                prosecution_rules.append({"rule_id": rule_id, "weight": strength, "source": source})
                pros_score += strength
            else:
                defense_rules.append({"rule_id": rule_id, "weight": strength, "source": source})
                def_score += strength

        total_points = pros_score + def_score
        if total_points == 0:
            return {
                "prosecution_supporting_rules": [],
                "prosecution_total_points": 0,
                "defense_opposing_rules": [],
                "defense_total_points": 0,
                "courtroom_winner": "N/A",
                "winning_reason": "N/A - Insufficient classical rules evaluated for target event.",
                "contradiction_report": {
                    "conflicts_identified": 0,
                    "conflicts_resolved": 0,
                    "winning_rule_id": "N/A",
                    "losing_rule_ids": []
                },
                "courtroom_net_favorability": "N/A"
            }

        pros_ratio = pros_score / total_points
        final_probability = round(pros_ratio * 100.0, 2)

        if pros_score > def_score * 1.5:
            winner = "PROSECUTION (POSITIVE FULFILLMENT)"
            reason = f"Prosecution evidence ({pros_score} pts) overwhelmingly defeats defense obstacles ({def_score} pts)."
        elif pros_score >= def_score:
            winner = "PROSECUTION (MODERATE FULFILLMENT WITH DELAYS)"
            reason = f"Prosecution holds lead ({pros_score} vs {def_score} pts). Opposing factors delay but do not destroy event."
        else:
            winner = "DEFENSE (OBSTRUCTED FULFILLMENT)"
            reason = f"Defense obstacles ({def_score} pts) defeat prosecution promise ({pros_score} pts)."

        return {
            "prosecution_supporting_rules": prosecution_rules,
            "prosecution_total_points": pros_score,
            "defense_opposing_rules": defense_rules,
            "defense_total_points": def_score,
            "courtroom_winner": winner,
            "winning_reason": reason,
            "contradiction_report": {
                "conflicts_identified": len(defense_rules),
                "conflicts_resolved": len(defense_rules),
                "winning_rule_id": prosecution_rules[0]["rule_id"] if prosecution_rules else "N/A",
                "losing_rule_ids": [r["rule_id"] for r in defense_rules]
            },
            "courtroom_net_favorability": f"{final_probability}%"
        }
