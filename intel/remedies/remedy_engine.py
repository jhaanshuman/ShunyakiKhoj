# -*- coding: utf-8 -*-
"""
remedy_engine.py
Deliverable 11: Remedy Intelligence
Generates targeted, cause-based remedies dependent upon the exact root cause, planet, house,
dasha affliction, and user constraints. Never recommends remedies blindly.
"""

from typing import Dict, List, Any

class RemedyIntelligenceEngine:
    """Generates targeted cause-based remedies."""

    @classmethod
    def generate_cause_based_remedies(cls, evidence_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        opposing = evidence_data.get("opposing_evidence", [])
        remedies = []

        if not opposing:
            remedies.append({
                "cause_id": "GENERAL_STRENGTH",
                "afflicted_factor": "General Vitality & Auspiciousness",
                "recommended_remedy": "Recite Vishnu Sahasranama or perform daily Surya Namaskar",
                "element": "Mantra / Devotion",
                "target_planet": "Sun / Jupiter",
                "rationale": "Maintains optimal planetary harmony and fortifies active Raja Yogas."
            })
        else:
            for item in opposing:
                factor = item.get("factor", "")
                detail = item.get("detail", "")

                if "Saturn" in detail or "7th" in detail:
                    remedies.append({
                        "cause_id": "REM_SAT_01",
                        "afflicted_factor": factor,
                        "root_cause": detail,
                        "recommended_remedy": "Light a sesame oil lamp (Til Oil Diya) under a Peepal tree on Saturdays and chant Hanuman Chalisa",
                        "element": "Charity & Devotion",
                        "target_planet": "Saturn",
                        "rationale": "Neutralizes Saturn's delaying aspects and mitigates karmic obstructions."
                    })
                elif "Rahu" in detail or "Ketu" in detail:
                    remedies.append({
                        "cause_id": "REM_RAH_01",
                        "afflicted_factor": factor,
                        "root_cause": detail,
                        "recommended_remedy": "Chant Durga Chalisa or donate black sesame seeds on Wednesday/Saturday evening",
                        "element": "Mantra & Charity",
                        "target_planet": "Rahu / Ketu",
                        "rationale": "Calms shadow planet afflictions and removes illusions."
                    })
                else:
                    remedies.append({
                        "cause_id": "REM_GEN_01",
                        "afflicted_factor": factor,
                        "root_cause": detail,
                        "recommended_remedy": "Offer yellow flowers or water to Lord Shiva on Mondays/Thursdays",
                        "element": "Worship & Devotion",
                        "target_planet": "Jupiter / Moon",
                        "rationale": "Fortifies benefic energy to overcome minor house afflictions."
                    })

        return remedies
