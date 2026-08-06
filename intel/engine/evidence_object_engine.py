# -*- coding: utf-8 -*-
"""
evidence_object_engine.py
Sprint 5 Rich Reusable Evidence Objects Engine
Transforms classical rules into rich, reusable evidence structures:
{
  "id": "RULE_VEH_014",
  "supports": "Vehicle Purchase",
  "weight": 28,
  "confidence": 0.92,
  "source": "Brihat Parashara Hora Shastra",
  "dependencies": ["4th House", "Venus"],
  "contradictions": [],
  "timing": ["Active Dasha"],
  "priority": "PRIMARY"
}
"""

from typing import Dict, List, Any

class RichEvidenceEngine:
    """Constructs rich reusable astrological evidence objects."""

    @classmethod
    def create_evidence_object(
        cls,
        rule_id: str,
        supports_event: str,
        confidence: float,
        strength: int,
        source: str,
        positive_impact: bool,
        dependencies: List[str] = None,
        contradictions: List[str] = None
    ) -> Dict[str, Any]:

        impact_type = "PROSECUTION_POSITIVE" if positive_impact else "DEFENSE_OBSTACLE"
        priority = "PRIMARY" if strength >= 85 else "SECONDARY"

        return {
            "id": rule_id,
            "rule_id": rule_id,
            "supports": supports_event,
            "supports_event": supports_event,
            "weight": strength,
            "strength": strength,
            "confidence": round(confidence, 2),
            "source": source,
            "dependencies": dependencies if dependencies else ["House Placement", "Planet Dignity"],
            "contradictions": contradictions if contradictions else [],
            "timing": ["Active Dasha Window"],
            "priority": priority,
            "impact_type": impact_type,
            "mathematical_contribution": f"+{strength} pts" if positive_impact else f"-{strength} pts"
        }
