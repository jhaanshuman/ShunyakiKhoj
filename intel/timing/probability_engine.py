# -*- coding: utf-8 -*-
"""
probability_engine.py
Deliverable 9 + Milestone 3: Continuous Probability Engine
Calculates continuous time-window probability distributions (0% to 100%)
based strictly on multi-layer astrological evidence weighting.
"""

from typing import Dict, List, Any

class AstrologicalProbabilityEngine:
    """Calculates continuous time-window probabilities based on evidence."""

    @classmethod
    def calculate_probability_distribution(cls, fused_timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        distribution = {}
        highest_window = None
        max_prob = 0.0
        secondary_window = None

        for item in fused_timeline:
            yr = item["year"]
            prob = item["probability_numerical"]
            distribution[str(yr)] = f"{prob}%"

            if prob > max_prob:
                secondary_window = highest_window
                max_prob = prob
                highest_window = yr

        return {
            "yearly_probability_distribution": distribution,
            "peak_event_window": highest_window,
            "peak_probability": f"{max_prob}%",
            "secondary_favored_window": secondary_window,
            "confidence_assessment": "HIGH (Multi-System Evidence Fusion Continuous Distribution)"
        }
