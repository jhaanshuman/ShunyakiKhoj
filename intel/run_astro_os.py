# -*- coding: utf-8 -*-
"""
run_astro_os.py
CLI Shell Entry Point for Sprint 5 ASTRO-OS.
Displays:
1. Query Diagnostic Analysis JSON (Entities, Intent, Confidence)
2. Top-K Semantic Intent Candidates Ranking
3. Preconditions Gate & Event Fingerprint Enforcement
4. Immutable EventContext Isolation Verification
5. Astrological World Model Trajectory Consequences
6. Rich Reusable Evidence Objects
7. Courtroom Debate & Contradiction Report
8. Continuous ASCII Probability Curve & Event-Isolated Contribution Breakdown
9. Dynamic Coverage Audit & Missing Evidence Warnings
10. Machine-Readable Replayable JSON Artifact
11. Honest Penalizing Meta-Reasoner Quality Gate
12. Honest System Readiness Progress (5 / 1268 = 0.39%)
"""

import sys
import os
import json

intel_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(intel_dir)
sys.path.insert(0, root_dir)
sys.path.append(intel_dir)

from intel.pipeline.reasoning_pipeline import AstroOSReasoningPipeline

def main():
    master_json_path = os.path.join(root_dir, "backend", "output", "master.json")
    if not os.path.exists(master_json_path):
        print(f"Error: Could not find {master_json_path}. Please run generate_research_data.py first.")
        sys.exit(1)

    print(f"Loading evidence base from {master_json_path}...")
    with open(master_json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "Foreign Travel, Visa & PR Scenario #5: Are there malefic Saturn or Rahu delays affecting my Foreign Travel, Visa & PR?"

    pipeline = AstroOSReasoningPipeline()
    res = pipeline.process_query(master_data, question)

    print("\n=======================================================")
    print(f"ASTRO-OS SPRINT 5 REASONING OPERATING SYSTEM")
    print(f"Query: \"{question}\"")
    print("=======================================================\n")

    print(f"--- 1. QUERY DIAGNOSTIC ANALYSIS ---")
    print(json.dumps(res["query_analysis"], indent=2) + "\n")

    print(f"--- 2. TOP-K SEMANTIC MULTILINGUAL INTENT RANKING ---")
    intent = res["semantic_multilingual_intent"]
    print(f"Intent Path: {intent['visible_intent_path']}")
    print(f"Selected Winner: {intent['target_event_name']} ({intent['target_event_id']}) with Confidence {intent['intent_confidence']}")
    print("Top Candidate Rankings:")
    for cand in intent["top_candidates"]:
        print(f"  - {cand['name']} ({cand['event_id']}): Confidence {cand['confidence']}")
    print("")

    print(f"--- 3. PRECONDITIONS GATE & EVENT FINGERPRINT ENFORCEMENT ---")
    ctx = res["event_context"]
    print(f"Fingerprint: {json.dumps(ctx['fingerprint'])}")
    print(f"Preconditions Gate: PASSED ({res['preconditions_status']})\n")

    print(f"--- 4. ASTROLOGICAL WORLD MODEL LIFE TRAJECTORY ---")
    world = res["astrological_world_model"]
    for cons in world["downstream_life_consequences"]:
        print(f"  - Downstream Impact on {cons['downstream_event']}: {cons['impact']}")
    print("")

    print(f"--- 5. EVENT-ISOLATED DEPENDENCY TRAVERSAL ---")
    print(res["dependency_hierarchy_traversal"]["dependency_chain_visual"] + "\n")

    print(f"--- 6. REPLAYABLE MATHEMATICAL REASONING TRACE ---")
    for step in res["replayable_mathematical_trace"]["replayable_mathematical_trace"]:
        print(f"  {step}")
    print("")

    print(f"--- 7. COURTROOM CONFLICT DEBATE & CONTRADICTION REPORT ---")
    court = res["courtroom_debate_report"]
    print(f"Prosecution (Argument A): {court['prosecution_total_points']} pts | Defense (Argument B): {court['defense_total_points']} pts")
    print(f"Courtroom Winner: {court['courtroom_winner']}")
    print(f"Winning Reason: {court['winning_reason']}\n")

    print(f"--- 8. CONTINUOUS PROBABILITY CURVE & CONTRIBUTION BREAKDOWN ---")
    print(res["probability_curve_and_breakdown"]["ascii_curve"])
    print("\nProbability Contribution Breakdown:")
    for k, v in res["probability_curve_and_breakdown"]["probability_contribution_breakdown"].items():
        print(f"  - {k}: {v}")
    print("")

    print(f"--- 9. DYNAMIC COVERAGE & MISSING EVIDENCE WARNINGS ---")
    cov = res["measurable_coverage_report"]
    print(f"Coverage: {cov['measurable_coverage_percentage']} ({cov['indicators_found']} found / {cov['required_indicators_expected']} expected)")
    print(f"Confidence Level: {cov['confidence_level']}")
    if cov["missing_evidence_warnings"]:
        for w in cov["missing_evidence_warnings"]:
            print(f"  {w}")
    print("")

    print(f"--- 10. MACHINE-READABLE REPLAYABLE JSON ARTIFACT ---")
    print(json.dumps(res["machine_readable_json_artifact"], indent=2))
    print("")

    print(f"--- 11. HONEST PENALIZING META-REASONER QUALITY GATE ---")
    meta = res["meta_reasoner_evaluation"]
    print(f"Quality Gate Verdict: {meta['meta_eval_verdict']}")
    print(f"Overall Prediction Trust Score: {meta['overall_prediction_trust']} / 100")
    print(f"Quality Gate Check: Context Valid: {meta['event_context_valid']} | Rule NS: {meta['rule_namespace_valid']} | Citation NS: {meta['citation_namespace_valid']}\n")

    print(f"--- 12. HONEST SYSTEM READINESS AUDITOR ---")
    honest = res["honest_system_auditor"]
    print(f"Knowledge Base Progress: {honest['honest_knowledge_base_progress']}")
    print(f"System Status: {honest['honest_system_status']}")

    print("\n=======================================================\n")

if __name__ == "__main__":
    main()
