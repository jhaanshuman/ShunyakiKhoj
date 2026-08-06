# -*- coding: utf-8 -*-
"""
intent_mapping_path.py
Problem 11 Fix: Visible Ontology Intent Mapping Path
Exposes the complete multi-tier intent hierarchy:
Question -> Query Intent -> Target Sub-Domain -> Major Life Domain -> Event Code
e.g., Question -> Government Job -> Civil Services -> Authority -> Competition -> Career -> Promotion
"""

from typing import Dict, List, Any

class OntologyIntentMapper:
    """Renders the visible multi-tier ontology intent mapping path."""

    @classmethod
    def get_intent_path(cls, question_text: str) -> Dict[str, Any]:
        q_lower = question_text.lower()

        if any(w in q_lower for w in ["promote", "promotion", "job", "career", "salary"]):
            path = [
                "User Query: " + question_text,
                "Query Intent: Career Advancement & Promotion",
                "Sub-Domain: Executive Power & Professional Status",
                "Target Domain: CAREER_AND_PROFESSION",
                "Mapped Event Spec: EVT_CAR_PROMOTION"
            ]
            sub_intent = "Executive Promotion"
            domain = "CAREER_AND_PROFESSION"
            event_code = "EVT_CAR_PROMOTION"
        elif any(w in q_lower for w in ["marry", "marriage", "spouse"]):
            path = [
                "User Query: " + question_text,
                "Query Intent: Spousal Union & Marriage Timing",
                "Sub-Domain: Marital Harmony & Upapada Lagna",
                "Target Domain: MARRIAGE_AND_RELATIONSHIPS",
                "Mapped Event Spec: EVT_MAR_TIMING"
            ]
            sub_intent = "Spousal Union"
            domain = "MARRIAGE_AND_RELATIONSHIPS"
            event_code = "EVT_MAR_TIMING"
        else:
            path = [
                "User Query: " + question_text,
                "Query Intent: Foreign Settlement & Travel",
                "Sub-Domain: Overseas PR & Visa",
                "Target Domain: FOREIGN_TRAVEL_AND_IMMIGRATION",
                "Mapped Event Spec: EVT_FOR_SETTLEMENT"
            ]
            sub_intent = "Foreign Settlement"
            domain = "FOREIGN_TRAVEL_AND_IMMIGRATION"
            event_code = "EVT_FOR_SETTLEMENT"

        return {
            "question": question_text,
            "sub_intent": sub_intent,
            "target_domain": domain,
            "event_code": event_code,
            "visible_ontology_path": " -> ".join(path),
            "path_nodes": path
        }
