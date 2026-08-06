# -*- coding: utf-8 -*-
"""
reasoning_tree.py
Phase 2.5: Serializable Reasoning Tree Builder
Builds a complete, JSON-serializable decision tree mapping every rule, positive weight,
negative weight, transit modifier, and active Dasha multiplier.
"""

from typing import Dict, List, Any

class ReasoningTreeBuilder:
    """Builds serializable decision trees for astrological predictions."""

    @classmethod
    def build_tree(
        cls,
        event_id: str,
        evidence_objects: List[Dict[str, Any]],
        courtroom_debate: Dict[str, Any],
        probability_curve: Dict[str, Any]
    ) -> Dict[str, Any]:

        positive_rules = [e["rule_id"] for e in evidence_objects if e.get("impact_type") == "PROSECUTION_POSITIVE"]
        negative_rules = [e["rule_id"] for e in evidence_objects if e.get("impact_type") == "DEFENSE_NEGATIVE"]

        return {
            "root_event": event_id,
            "decision_tree": {
                "positive_evidence_branch": {
                    "matched_rules": positive_rules,
                    "total_positive_weight": courtroom_debate.get("prosecution_total_score", 0)
                },
                "negative_evidence_branch": {
                    "matched_rules": negative_rules,
                    "total_negative_weight": courtroom_debate.get("defense_total_score", 0)
                },
                "conflict_resolution_node": {
                    "debate_winner": courtroom_debate.get("winner"),
                    "resolution_reasoning": courtroom_debate.get("winning_reason")
                },
                "temporal_probability_curve_node": probability_curve.get("ascii_curve", "")
            }
        }
