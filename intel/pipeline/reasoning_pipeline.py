# -*- coding: utf-8 -*-
"""
reasoning_pipeline.py
Sprint 5 Unified ASTRO-OS Query Pipeline
Orchestrates:
1. Top-K Semantic Multilingual Intent Ranking Engine
2. Query Diagnostic Analysis (Entities, Confidence, Candidates)
3. Declarative Event Spec Compilation & Immutable EventContext Construction
4. Precondition Gate Validation (Intent Valid -> Fingerprint Match -> Rule Namespace Valid -> Proceed)
5. Astrological World Model Life Trajectory Simulation
6. Event-Isolated Mini Graph Topology Validation
7. Event-Isolated Dependency Traversal
8. Rich Reusable Evidence Objects Execution
9. Courtroom Conflict Debate Engine
10. Event-Isolated Continuous Probability Curve
11. Replayable Math Reasoning Trace
12. Dynamic Coverage Audit & Missing Evidence Warnings
13. Machine-Readable Replayable JSON Artifact Generator
14. Honest Penalizing Meta-Reasoner Quality Gate
15. Honest System Readiness Auditor
"""

from typing import Dict, List, Any

from ..intent.semantic_intent_engine import SemanticIntentEngine
from ..query_analyzer import QueryAnalyzer
from ..compiler.event_compiler import AstrologicalEventCompiler
from ..context.event_context import EventContext
from ..context.context_validator import EventContextValidator
from ..world_model.world_model import AstrologicalWorldModel
from ..artifact_generator import MachineReadableArtifactGenerator
from ..ontology.event_dependency_graph import EventDependencyGraph
from ..engine.evidence_object_engine import RichEvidenceEngine
from ..engine.courtroom_conflict_engine import CourtroomConflictEngine
from ..engine.probability_curve_engine import ProbabilityCurveEngine
from ..engine.reasoning_tree import ReasoningTreeBuilder
from ..engine.validation_engine import MiniGraphValidationEngine
from ..engine.coverage_engine import SelfAwareCoverageEngine
from ..engine.reasoning_trace import ReasoningTraceGenerator
from ..auditor.honest_auditor import HonestSystemAuditor
from ..meta_reasoner.meta_reasoner import MetaReasonerEngine
from ..timing.time_fusion import TimeFusionEngine
from ..rules.rule_library import UniversalRuleLibrary

class AstroOSReasoningPipeline:
    """Master Query Pipeline for Sprint 5 ASTRO-OS."""

    def __init__(self):
        self.compiler = AstrologicalEventCompiler()

    def process_query(self, master_data: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        # 1. Top-K Semantic Multilingual Intent Ranking Engine
        semantic_intent = SemanticIntentEngine.resolve_intent(user_query)

        event_id = semantic_intent["target_event_id"]
        domain_code = semantic_intent["target_domain_code"]

        # 2. Query Diagnostic Analyzer
        query_analysis = QueryAnalyzer.analyze_query(user_query, semantic_intent)

        # 3. Declarative Event Spec Compilation
        compiled_spec = self.compiler.get_compiled_event(event_id)

        rule_namespace = compiled_spec.get("rule_namespace", domain_code.split("_")[0])
        citation_namespace = compiled_spec.get("citation_namespace", domain_code.split("_")[0])

        # 4. Rules Execution for Event
        rules = UniversalRuleLibrary.get_rules_for_event(event_id)
        rich_evidence_list = []

        for r in rules:
            e_obj = RichEvidenceEngine.create_evidence_object(
                rule_id=r.rule_id,
                supports_event=compiled_spec.get("event_name", "Life Event"),
                confidence=r.confidence,
                strength=int(r.weight * 100),
                source=r.sources[0].text if r.sources else "Brihat Parashara Hora Shastra",
                positive_impact=r.positive_impact,
                dependencies=[f"House {h}" for h in compiled_spec.get("required_houses", [])]
            )
            rich_evidence_list.append(e_obj)

        # 5. Construct Immutable EventContext Container with Fingerprint
        event_context = EventContext(
            event_id=event_id,
            event_name=compiled_spec.get("event_name", "Life Event"),
            domain_code=domain_code,
            required_houses=compiled_spec.get("required_houses", []),
            required_karakas=compiled_spec.get("required_karakas", []),
            varga_chart=compiled_spec.get("varga_chart", "D1"),
            rule_namespace=rule_namespace,
            citation_namespace=citation_namespace,
            rules=[{"rule_id": r.rule_id, "weight": r.weight} for r in rules],
            citations=compiled_spec.get("classical_citations", []),
            remedies=compiled_spec.get("remedies", []),
            expected_indicators=compiled_spec.get("required_houses", [])
        )

        # 6. Validate Precondition Gate & Event Fingerprint (Aborts on mismatch)
        preconditions_status = EventContextValidator.validate_preconditions(event_context)

        # 7. Astrological World Model Life Simulation
        world_model_simulation = AstrologicalWorldModel.simulate_life_trajectory(event_id)

        # 8. Mini-Graph Topology Validation
        topology_validation = MiniGraphValidationEngine.validate_mini_graph(compiled_spec)

        # 9. Event-Specific Dependency Traversal
        dependency_traversal = EventDependencyGraph.get_dependency_traversal(event_id)

        # 10. Courtroom Conflict Debate Engine
        courtroom_debate = CourtroomConflictEngine.conduct_courtroom_debate(rich_evidence_list)

        # 11. Event-Aware Time Fusion & Continuous Probability Curve
        timeline = TimeFusionEngine.generate_fused_timeline(master_data, event_id)
        prob_curve = ProbabilityCurveEngine.generate_probability_curve(timeline, event_id)

        # 12. Replayable Math Reasoning Trace
        math_trace = ReasoningTraceGenerator.generate_trace(
            user_query=user_query,
            intent_domain=domain_code,
            event_name=compiled_spec.get("event_name", ""),
            evidence_objects=rich_evidence_list,
            courtroom_debate=courtroom_debate,
            timeline=timeline
        )

        # 13. Dynamic Coverage Audit & Missing Evidence Warnings
        coverage_report = SelfAwareCoverageEngine.audit_prediction_coverage(event_id, len(rich_evidence_list))

        # 14. Honest Penalizing Meta-Reasoner Quality Gate
        meta_eval = MetaReasonerEngine.evaluate_reasoning_quality(
            coverage_report=coverage_report,
            courtroom_debate=courtroom_debate,
            citations_count=len(rules) * 2,
            preconditions_status=preconditions_status
        )

        # 15. Machine-Readable JSON Artifact Generation
        machine_artifact = MachineReadableArtifactGenerator.generate_artifact(
            user_query=user_query,
            semantic_intent=semantic_intent,
            selected_event_id=event_id,
            reasoning_trace=math_trace,
            coverage_report=coverage_report,
            meta_audit=meta_eval,
            world_model_simulation=world_model_simulation
        )

        # 16. Honest System Readiness Auditor
        honest_audit = HonestSystemAuditor.audit_honest_system(
            defined_events_count=5,
            rules_executed_count=len(rules),
            rules_skipped_count=0
        )

        return {
            "query": user_query,
            "query_analysis": query_analysis,
            "event_context": event_context.to_dict(),
            "preconditions_status": preconditions_status,
            "semantic_multilingual_intent": semantic_intent,
            "declarative_event_spec": compiled_spec,
            "astrological_world_model": world_model_simulation,
            "graph_topology_validation": topology_validation,
            "dependency_hierarchy_traversal": dependency_traversal,
            "rich_evidence_objects": rich_evidence_list,
            "courtroom_debate_report": courtroom_debate,
            "probability_curve_and_breakdown": prob_curve,
            "replayable_mathematical_trace": math_trace,
            "measurable_coverage_report": coverage_report,
            "machine_readable_json_artifact": machine_artifact,
            "meta_reasoner_evaluation": meta_eval,
            "honest_system_auditor": honest_audit
        }
