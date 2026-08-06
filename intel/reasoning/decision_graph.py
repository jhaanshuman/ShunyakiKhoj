# -*- coding: utf-8 -*-
"""
decision_graph.py
Deliverable 13 & 14: Decision Graph Execution Pipeline & Explainability Layer
Orchestrates the complete evidence-based reasoning pipeline for any life question:
Question -> Intent -> Event -> Evidence -> Weighted Analysis -> Conflict Resolution -> Timeline -> Probability -> Explanation -> Remedies -> Classical Citations -> Debug Log
"""

from typing import Dict, List, Any
from ..intent.intent_engine import QuestionIntentEngine
from ..ontology.event_ontology import EventOntology
from ..rules.rule_library import UniversalRuleLibrary
from ..rules.rule_weighting import RuleWeightingEngine
from .evidence_collector import UniversalEvidenceCollector
from .conflict_resolver import ContradictionResolver
from ..timing.time_fusion import TimeFusionEngine
from ..timing.probability_engine import AstrologicalProbabilityEngine
from .explanation_engine import ExplanationEngine
from ..remedies.remedy_engine import RemedyIntelligenceEngine

class AstrologicalDecisionGraph:
    """Master Decision Graph pipeline orchestrating evidence-based astrological reasoning."""

    @classmethod
    def execute_reasoning_pipeline(cls, master_obj: Dict[str, Any], question_text: str) -> Dict[str, Any]:
        debug_logs = []
        debug_logs.append("1. Step 1: Question Intent Parsing")
        intent = QuestionIntentEngine.parse_question_intent(question_text)

        event_id = intent["target_event_id"]
        debug_logs.append(f"2. Step 2: Mapped Event '{event_id}' ({intent['target_event_name']})")

        # Gather Event Spec & Classical Rules
        event_spec = EventOntology.get_event_spec(event_id)
        classical_rules = UniversalRuleLibrary.get_rules_for_event(event_id)
        debug_logs.append(f"3. Step 3: Loaded {len(classical_rules)} Classical Rules with Source Citations")

        # Step 4: Collect Evidence
        evidence = UniversalEvidenceCollector.collect_evidence_for_event(master_obj, event_id)
        debug_logs.append(f"4. Step 4: Collected Evidence ({evidence['supporting_evidence_count']} Supporting, {evidence['opposing_evidence_count']} Opposing)")

        # Step 5: Conflict Resolution
        resolution = ContradictionResolver.resolve_conflicts(evidence)
        debug_logs.append(f"5. Step 5: Resolved Evidence Conflicts (Net Favorability: {resolution['net_favorability_percentage']}%)")

        # Step 6: Time Fusion & Continuous Probability
        fused_timeline = TimeFusionEngine.generate_fused_timeline(master_obj, event_id)
        probability_dist = AstrologicalProbabilityEngine.calculate_probability_distribution(fused_timeline)
        debug_logs.append(f"6. Step 6: Computed Continuous Probability (Peak Window: {probability_data_key if 'probability_data_key' in locals() else probability_dist.get('peak_event_window')})")

        # Step 7: Explanation Engine
        explanation = ExplanationEngine.generate_explanation(question_text, intent, resolution, probability_dist, evidence)
        debug_logs.append("7. Step 7: Generated Structured Astrological Reasoning (WHAT, WHY, HOW, WHEN)")

        # Step 8: Remedy Intelligence
        remedies = RemedyIntelligenceEngine.generate_cause_based_remedies(evidence)
        debug_logs.append(f"8. Step 8: Generated {len(remedies)} Cause-Based Remedies")

        # Step 9: Classical Source Citations
        citations = []
        for r in classical_rules:
            for src in r.sources:
                citations.append({
                    "rule_id": r.rule_id,
                    "rule_name": r.name,
                    "classical_text": src.text,
                    "chapter": src.chapter,
                    "verse": src.verse,
                    "confidence": r.confidence
                })

        return {
            "status": "SUCCESS",
            "question": question_text,
            "intent": intent,
            "event_specification": {
                "event_id": event_spec.event_id,
                "event_name": event_spec.event_name,
                "primary_houses": event_spec.primary_houses,
                "primary_karakas": event_spec.primary_karakas
            },
            "evidence_summary": evidence,
            "conflict_resolution": resolution,
            "probability_timeline": fused_timeline,
            "probability_distribution": probability_dist,
            "explanation": explanation,
            "cause_based_remedies": remedies,
            "classical_source_citations": citations,
            "execution_trace_debug_logs": debug_logs
        }
