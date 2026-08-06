# -*- coding: utf-8 -*-
"""
test_astro_os.py
Unit & Integration tests verifying ASTRO-OS Declarative Compiler and Reasoning OS.
"""

import sys
import os
import json

intel_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(intel_dir)
sys.path.insert(0, root_dir)
sys.path.append(intel_dir)

from intel.pipeline.reasoning_pipeline import AstroOSReasoningPipeline

def test_astro_os():
    master_json_path = os.path.join(root_dir, "backend", "output", "master.json")
    with open(master_json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    pipeline = AstroOSReasoningPipeline()

    # Query 1: Promotion
    res1 = pipeline.process_query(master_data, "Will I get a promotion in my job?")
    assert res1["mini_graph_validation"]["validation_status"] == "PASS"
    assert len(res1["rich_evidence_objects"]) > 0
    assert "prosecution_total_score" in res1["courtroom_debate_verdict"]
    assert "ascii_curve" in res1["probability_curve"]
    assert res1["self_audit_report"]["self_audit_status"] == "PASSED ALL 10 AUDIT CHECKS"
    print("Test 1 PASS: ASTRO-OS Promotion Query Pipeline & Courtroom Debate")

    # Query 2: Marriage
    res2 = pipeline.process_query(master_data, "When will I get married?")
    assert res2["mini_graph_validation"]["validation_status"] == "PASS"
    assert "reasoning_tree" in res2
    print("Test 2 PASS: ASTRO-OS Marriage Query Declarative Compiler Pipeline")

if __name__ == "__main__":
    test_astro_os()
    print("\nALL ASTRO-OS SYSTEM TESTS PASSED SUCCESSFULLY!")
