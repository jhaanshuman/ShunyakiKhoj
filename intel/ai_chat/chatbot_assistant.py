# -*- coding: utf-8 -*-
"""
chatbot_assistant.py
Milestone 4: Conversational Astrological Reasoning Assistant
Accepts natural language life questions, executes the Astrological Decision Graph,
and synthesizes evidence-based, explainable natural language answers with exact timing,
classical text citations, and cause-based remedies.
"""

from typing import Dict, List, Any
import json
import os
from ..reasoning.decision_graph import AstrologicalDecisionGraph

class AstrologicalChatbotAssistant:
    """Conversational AI Reasoning Assistant for Astrological Life Queries."""

    def __init__(self, master_data: Dict[str, Any]):
        self.master_data = master_data

    def answer_life_question(self, user_question: str) -> Dict[str, Any]:
        reasoning = AstrologicalDecisionGraph.execute_reasoning_pipeline(self.master_data, user_question)

        intent = reasoning["intent"]
        resolution = reasoning["conflict_resolution"]
        prob_dist = reasoning["probability_distribution"]
        timeline = reasoning["probability_timeline"]
        explanation = reasoning["explanation"]
        remedies = reasoning["cause_based_remedies"]
        citations = reasoning["classical_source_citations"]

        # Synthesize Human-Readable Natural Language Response
        nl_response = []
        nl_response.append(f"### ASTROLOGICAL REASONING RESPONSE: \"{user_question}\"")
        nl_response.append(f"**Target Domain**: {intent['parsed_domain']} ({intent['target_event_name']})")
        nl_response.append(f"**Astrological Conclusion**: {resolution['final_conclusion']} (Net Favorability: {resolution['net_favorability_percentage']}%)")
        nl_response.append("")

        nl_response.append("#### [1] Exact Timeframe & Continuous Probability Timeline:")
        for t in timeline:
            star_badge = "[PEAK WINDOW]" if t['window_status'] == "PRIMARY PEAK WINDOW" else ""
            nl_response.append(f"- **Year {t['year']}**: **{t['fused_probability']}** ({t['active_dasha']} Dasha, {t['transit_influence']}) {star_badge}")
        nl_response.append(f"-> **Peak Opportunity Window**: **{prob_dist['peak_event_window']}** (Peak Probability: **{prob_dist['peak_probability']}**)")
        nl_response.append("")

        nl_response.append("#### [2] Astrological Reasoning Breakdown (WHAT, WHY, HOW, WHEN):")
        nl_response.append(f"- **WHAT (Outcome)**: {explanation['WHAT_OUTCOME']}")
        nl_response.append(f"- **WHY (Root Cause)**: {explanation['WHY_ASTROLOGICAL_REASON']}")
        nl_response.append(f"- **HOW (Planetary Dynamics)**: {explanation['HOW_PLANETARY_DYNAMICS']}")
        nl_response.append(f"- **WHEN (Timeframe)**: {explanation['WHEN_PEAK_TIMEFRAME']}")
        nl_response.append(f"- **WHY NOT (Obstacles)**: {explanation['WHY_NOT_OBSTACLES']}")
        nl_response.append(f"- **WHAT IMPROVES**: {explanation['WHAT_IMPROVES']}")
        nl_response.append(f"- **WHAT WORSENS**: {explanation['WHAT_WORSENS']}")
        nl_response.append("")

        nl_response.append("#### [3] Classical Textual Citations & Academic Sources:")
        for c in citations:
            nl_response.append(f"- **{c['rule_name']}**: *{c['classical_text']}* (Chapter {c['chapter']}, Verse {c['verse']}) -- Confidence: {int(c['confidence']*100)}%")
        nl_response.append("")

        nl_response.append("#### [4] Cause-Based Targeted Remedies:")
        for r in remedies:
            nl_response.append(f"- **For {r['afflicted_factor']}**: {r['recommended_remedy']} *(Target: {r['target_planet']}, Rationale: {r['rationale']})*")

        formatted_markdown = "\n".join(nl_response)

        return {
            "question": user_question,
            "markdown_formatted_response": formatted_markdown,
            "raw_reasoning_graph": reasoning
        }
