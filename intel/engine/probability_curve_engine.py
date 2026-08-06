# -*- coding: utf-8 -*-
"""
probability_curve_engine.py
ASTRO-OS 2.0 Event-Aware Probability Curve Generator
Generates event-isolated probability point contribution breakdowns:
- Vehicle: Chaturthamsha D4 (9%), Venus/Mars Karaka (18%), 4th House/Lord (38%)
- Childbirth: Saptamsha D7 (9%), Jupiter Karaka (18%), 5th House/Lord (38%)
- Career: Dashamsha D10 (9%), Sun Karaka (18%), 10th House/Lord (38%)
- Marriage: Navamsha D9 (9%), Venus Karaka (18%), 7th House/Lord (38%)
"""

from typing import Dict, List, Any

class ProbabilityCurveEngine:
    """Generates continuous probability curves with event-isolated point contribution breakdowns."""

    @classmethod
    def generate_probability_curve(cls, timeline: List[Dict[str, Any]], event_id: str = "EVT_CAR_PROMOTION") -> Dict[str, Any]:
        ascii_lines = []
        numerical_map = {}

        for item in timeline:
            yr = item["year"]
            prob = item["probability_numerical"]
            numerical_map[str(yr)] = f"{prob}%"

            blocks_count = max(1, int(prob / 10.0))
            bar = "#" * blocks_count
            peak_marker = " [PEAK WINDOW]" if prob >= 85.0 else ""
            ascii_lines.append(f"{yr} {bar} ({prob}%){peak_marker}")

        ascii_curve = "\n".join(ascii_lines)

        target = event_id.upper()

        if "VEHICLE" in target or "PROP" in target:
            varga_label = "Divisional_Varga_Chaturthamsha_D4"
            karaka_label = "Vehicle_Karaka_Venus_Mars_Strength"
            house_label = "Natal_Promise_4th_House_D1"
        elif "CHI" in target or "CHILD" in target:
            varga_label = "Divisional_Varga_Saptamsha_D7"
            karaka_label = "Progeny_Karaka_Jupiter_Strength"
            house_label = "Natal_Promise_5th_House_D1"
        elif "MAR" in target or "MARRIAGE" in target:
            varga_label = "Divisional_Varga_Navamsha_D9"
            karaka_label = "Spouse_Karaka_Venus_Jupiter_Strength"
            house_label = "Natal_Promise_7th_House_D1"
        else:
            varga_label = "Divisional_Varga_Dashamsha_D10"
            karaka_label = "Career_Karaka_Sun_Saturn_Strength"
            house_label = "Natal_Promise_10th_House_D1"

        contribution_breakdown = {
            house_label: "38%",
            "Active_Mahadasha_Antardasha": "25%",
            karaka_label: "18%",
            varga_label: "9%",
            "Active_Raja_Dhana_Yogas": "8%",
            "KP_Sublord_Significators": "0%",
            "Total_Fused_Probability": "98%"
        }

        return {
            "ascii_curve": ascii_curve,
            "numerical_curve": numerical_map,
            "probability_contribution_breakdown": contribution_breakdown
        }
