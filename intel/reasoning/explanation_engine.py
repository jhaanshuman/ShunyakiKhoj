# -*- coding: utf-8 -*-
"""
explanation_engine.py
Deliverable 10: Explanation Engine
Synthesizes comprehensive explanations answering:
WHAT (Outcome), WHY (Astrological Root Cause), HOW (Planetary Dynamics), WHEN (Peak Window),
WHY NOT (Obstacles), WHAT IMPROVES, and WHAT WORSENS.
"""

from typing import Dict, List, Any

class ExplanationEngine:
    """Generates structured astrological reasoning explanations."""

    @classmethod
    def generate_explanation(
        cls,
        user_question: str,
        intent_data: Dict[str, Any],
        resolution_data: Dict[str, Any],
        probability_data: Dict[str, Any],
        evidence_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        event_name = intent_data.get("target_event_name", "Life Event")
        conclusion = resolution_data.get("final_conclusion", "")
        peak_window = probability_data.get("peak_event_window", 2028)

        supp_list = [f"• {e['factor']}: {e['detail']}" for e in evidence_data.get("supporting_evidence", [])]
        opp_list = [f"• {e['factor']}: {e['detail']}" for e in evidence_data.get("opposing_evidence", [])]

        what_str = f"Regarding '{user_question}': The astrological outcome is {conclusion}."
        why_str = f"Primary astrological drivers: \n" + "\n".join(supp_list) if supp_list else "Favorable planetary placements in Natal Chart."
        how_str = f"Planetary dynamics operate via active Mahadasha alignment, strong sign lord dignities, and Ashtakvarga Bindu strength."
        when_str = f"The most favorable peak timeframe is {peak_window} (Probability: {probability_data.get('peak_probability', '84%')})."
        why_not_str = f"Potential obstacles/delays: \n" + ("\n".join(opp_list) if opp_list else "None major. Minor transiting aspects require patience.")
        what_improves_str = "Fulfillment probability improves significantly during Jupiter transits and when targeted remedies for opposing factors are practiced."
        what_worsens_str = "Neglecting Saturn/Rahu remediations or acting rashly during adverse Antardashas increases temporary friction."

        return {
            "WHAT_OUTCOME": what_str,
            "WHY_ASTROLOGICAL_REASON": why_str,
            "HOW_PLANETARY_DYNAMICS": how_str,
            "WHEN_PEAK_TIMEFRAME": when_str,
            "WHY_NOT_OBSTACLES": why_not_str,
            "WHAT_IMPROVES": what_improves_str,
            "WHAT_WORSENS": what_worsens_str
        }
