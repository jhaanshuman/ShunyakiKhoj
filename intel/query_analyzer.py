# -*- coding: utf-8 -*-
"""
query_analyzer.py
Sprint 5 Query Analyzer Module
Generates structured query analysis diagnostic JSON before reasoning begins:
{
  "query": "...",
  "entities": [...],
  "intent": "...",
  "confidence": 98,
  "candidate_events": [...]
}
"""

from typing import Dict, List, Any

class QueryAnalyzer:
    """Analyzes user query and extracts entities, candidate events, and intent confidence."""

    @classmethod
    def analyze_query(cls, user_query: str, semantic_intent: Dict[str, Any]) -> Dict[str, Any]:
        q_lower = user_query.lower()
        entities = []

        keywords = ["xuv", "car", "vehicle", "baby", "child", "marriage", "visa", "foreign", "job", "promotion", "salary"]
        for kw in keywords:
            if kw in q_lower:
                entities.append(kw.upper())

        return {
            "query": user_query,
            "entities": entities if entities else ["GENERAL_LIFE_QUERY"],
            "intent": semantic_intent.get("target_domain_code"),
            "confidence": semantic_intent.get("intent_confidence"),
            "candidate_events": semantic_intent.get("top_candidates", []),
            "analysis_status": "PASSED"
        }
