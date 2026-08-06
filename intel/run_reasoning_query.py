# -*- coding: utf-8 -*-
"""
run_reasoning_query.py
CLI Entry Point for the Astrological Reasoning Engine (intel/).
Reads backend evidence (`backend/output/master.json`), accepts any user life question,
and executes the 15-deliverable Astrological Reasoning & Chatbot Assistant.
"""

import sys
import os
import json

intel_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(intel_dir)
sys.path.insert(0, root_dir)
sys.path.append(intel_dir)

from intel.ai_chat.chatbot_assistant import AstrologicalChatbotAssistant
from intel.auditor.coverage_analyzer import KnowledgeCoverageAnalyzer

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
        question = "When will I get married?"

    assistant = AstrologicalChatbotAssistant(master_data)
    response = assistant.answer_life_question(question)

    print("\n=======================================================")
    print("ASTROLOGICAL REASONING ENGINE (intel/)")
    print("=======================================================\n")

    print(response["markdown_formatted_response"])

    print("\n-------------------------------------------------------")
    print("Knowledge Coverage Auditor Report:")
    audit_report = KnowledgeCoverageAnalyzer.audit_coverage()
    print(json.dumps(audit_report, indent=2))
    print("-------------------------------------------------------\n")

if __name__ == "__main__":
    main()
