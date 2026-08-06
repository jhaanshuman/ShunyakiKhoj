# -*- coding: utf-8 -*-
"""
artifact_generator.py
ASTRO-OS 2.0 Machine-Readable Replayable JSON Artifact Generator
Generates a complete JSON artifact for debugging every run:
{
  "query": "...",
  "intent": "...",
  "candidate_events": [...],
  "selected_event": "...",
  "selection_reason": "...",
  "reasoning_trace": "...",
  "coverage": "...",
  "meta_audit": "..."
}
"""

from typing import Dict, List, Any
import json

class MachineReadableArtifactGenerator:
    """Generates structured machine-readable JSON debugging artifacts."""

    @classmethod
    def generate_artifact(
        cls,
        user_query: str,
        semantic_intent: Dict[str, Any],
        selected_event_id: str,
        reasoning_trace: Dict[str, Any],
        coverage_report: Dict[str, Any],
        meta_audit: Dict[str, Any],
        world_model_simulation: Dict[str, Any]
    ) -> Dict[str, Any]:

        return {
            "query": user_query,
            "intent": semantic_intent.get("target_domain_code"),
            "candidate_events": semantic_intent.get("top_candidates", []),
            "selected_event": selected_event_id,
            "selection_reason": f"Matched keywords in {semantic_intent.get('target_event_name')}",
            "world_model_trajectory": world_model_simulation.get("downstream_life_consequences", []),
            "reasoning_trace": reasoning_trace.get("replayable_mathematical_trace", []),
            "coverage": coverage_report.get("measurable_coverage_percentage"),
            "meta_audit": meta_audit.get("overall_prediction_trust")
        }
