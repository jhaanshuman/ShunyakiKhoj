# -*- coding: utf-8 -*-
"""
Schema Validator v5.0.
Validates the universal JSON output against the enterprise v5.0 schema.
"""

from typing import Dict, Any, List

REQUIRED_V5_TOP_LEVEL_KEYS = [
    "engine_metadata", "input", "validation", "astronomy", "birth",
    "planets", "houses", "vargas", "strength", "aspects", "conjunctions",
    "yogas", "doshas", "dashas", "transits", "argala", "karakas",
    "jaimini", "kp", "panchanga", "matching", "house_analysis",
    "rule_engine", "domain_engine", "timeline", "prediction_index",
    "graphs", "tables", "statistics", "knowledge", "ai_context", "metadata"
]

class SchemaValidator:
    """Validates Master Horoscope Object v5.0 compliance."""

    @classmethod
    def validate_v5_output(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Audit top-level structure and completeness."""
        missing_keys = [k for k in REQUIRED_V5_TOP_LEVEL_KEYS if k not in data]
        present_keys = [k for k in REQUIRED_V5_TOP_LEVEL_KEYS if k in data]

        is_valid = len(missing_keys) == 0

        return {
            "is_valid": is_valid,
            "version": "5.0.0",
            "total_required_keys": len(REQUIRED_V5_TOP_LEVEL_KEYS),
            "present_keys_count": len(present_keys),
            "missing_keys": missing_keys,
            "completeness_percentage": round((len(present_keys) / len(REQUIRED_V5_TOP_LEVEL_KEYS)) * 100.0, 1)
        }
