# -*- coding: utf-8 -*-
"""
test_intel_pipeline.py
Unit tests verifying the Astrological Reasoning Engine (intel/).
"""

import sys
import os
import json

intel_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(intel_dir)
sys.path.insert(0, root_dir)
sys.path.append(intel_dir)

from intel.reasoning.decision_graph import AstrologicalDecisionGraph
from intel.auditor.coverage_analyzer import KnowledgeCoverageAnalyzer

def test_pipeline():
    master_json_path = os.path.join(root_dir, "backend", "output", "master.json")
    with open(master_json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    # Test Question 1: Marriage
    res_mar = AstrologicalDecisionGraph.execute_reasoning_pipeline(master_data, "When will I get married?")
    assert res_mar["status"] == "SUCCESS"
    assert "explanation" in res_mar
    assert len(res_mar["classical_source_citations"]) > 0
    print("Test 1 PASS: Marriage Question Reasoning Pipeline")

    # Test Question 2: Career
    res_car = AstrologicalDecisionGraph.execute_reasoning_pipeline(master_data, "Why am I unable to get promotion?")
    assert res_car["status"] == "SUCCESS"
    assert "cause_based_remedies" in res_car
    print("Test 2 PASS: Career Question Reasoning Pipeline")

    # Audit Check
    audit = KnowledgeCoverageAnalyzer.audit_coverage()
    assert audit["total_domains_audited"] > 0
    print("Test 3 PASS: Knowledge Coverage Auditor Check")

if __name__ == "__main__":
    test_pipeline()
    print("\nALL INTEL PIPELINE UNIT TESTS PASSED SUCCESSFULLY!")
