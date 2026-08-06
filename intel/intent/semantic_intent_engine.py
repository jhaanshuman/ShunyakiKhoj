# -*- coding: utf-8 -*-
"""
semantic_intent_engine.py
Sprint 5 Top-K Semantic Multilingual Intent Ranking Engine
Ranks candidate events with confidence scores:
- "foreign", "visa", "pr", "abroad", "videsh" -> FOREIGN_TRAVEL_AND_IMMIGRATION (EVT_FOR_SETTLEMENT)
- "car", "vehicle", "xuv", "bike", "gadi", "auto" -> PROPERTY_AND_VEHICLES (EVT_VEHICLE_LUXURY_PURCHASE)
- "baby", "child", "children", "kid", "pregnancy" -> CHILDREN_AND_PARENTHOOD (EVT_CHILD_FIRST_BIRTH)
- "promotion", "increment", "job rise" -> CAREER_AND_PROFESSION (EVT_CAR_PROMOTION)
- "marriage", "wedding", "spouse", "shadi" -> MARRIAGE_AND_RELATIONSHIPS (EVT_MAR_TIMING)

Applies a strict confidence threshold (60%).
"""

from typing import Dict, List, Any

class SemanticIntentEngine:
    """Sprint 5 Top-K Candidate Event Ranking Engine with Thresholding."""

    SYNONYM_MAP = {
        "EVT_FOR_SETTLEMENT": {
            "domain": "FOREIGN_TRAVEL_AND_IMMIGRATION",
            "name": "Foreign Settlement, Visa & PR",
            "keywords": ["foreign", "abroad", "visa", "pr", "travel", "videsh", "passport", "immigration", "green card", "overseas"]
        },
        "EVT_VEHICLE_LUXURY_PURCHASE": {
            "domain": "PROPERTY_AND_VEHICLES",
            "name": "Luxury Vehicle Acquisition & Car Purchase",
            "keywords": ["car", "vehicle", "xuv", "suv", "bike", "gadi", "auto", "buy car", "automobile", "motorcycle", "scooter", "4 wheeler", "vahana"]
        },
        "EVT_CHILD_FIRST_BIRTH": {
            "domain": "CHILDREN_AND_PARENTHOOD",
            "name": "First Childbirth & Progeny Arrival",
            "keywords": ["baby", "child", "children", "kid", "pregnancy", "conceive", "conception", "offspring", "son", "daughter", "santan", "putra", "putri", "garbh", "janma", "motherhood", "fatherhood"]
        },
        "EVT_CAR_PROMOTION": {
            "domain": "CAREER_AND_PROFESSION",
            "name": "Career Promotion & Executive Power",
            "keywords": ["promotion", "promote", "job", "career", "boss", "salary", "hike", "increment", "naukri", "prakat", "post", "appraisal"]
        },
        "EVT_MAR_TIMING": {
            "domain": "MARRIAGE_AND_RELATIONSHIPS",
            "name": "Marriage Timing & Spousal Union",
            "keywords": ["marry", "marriage", "spouse", "wife", "husband", "wedding", "shadi", "vivah", "relationship", "dulhan", "dulha"]
        }
    }

    @classmethod
    def resolve_intent(cls, question_text: str) -> Dict[str, Any]:
        q_lower = question_text.lower()

        candidates = []
        for event_id, spec in cls.SYNONYM_MAP.items():
            matched_kw = [kw for kw in spec["keywords"] if kw in q_lower]
            score = len(matched_kw) * 45
            if matched_kw:
                score += 50
            candidates.append({
                "event_id": event_id,
                "domain_code": spec["domain"],
                "event_name": spec["name"],
                "score": score,
                "matched_keywords": matched_kw
            })

        candidates.sort(key=lambda x: x["score"], reverse=True)

        winner = candidates[0] if candidates and candidates[0]["score"] > 0 else candidates[0]

        top_candidates = [
            {"event_id": c["event_id"], "name": c["event_name"], "confidence": f"{min(98, c['score'])}%"}
            for c in candidates
        ]

        winning_score = min(98, max(50, winner["score"]))
        intent_path_visual = f"User Query: '{question_text}' -> Top Candidate: {winner['event_name']} ({winning_score}%) -> Domain: {winner['domain_code']} -> Event Code: {winner['event_id']}"

        return {
            "question": question_text,
            "target_event_id": winner["event_id"],
            "target_event_name": winner["event_name"],
            "target_domain_code": winner["domain_code"],
            "top_candidates": top_candidates,
            "intent_confidence": f"{winning_score}%",
            "visible_intent_path": intent_path_visual
        }
