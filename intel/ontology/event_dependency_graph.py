# -*- coding: utf-8 -*-
"""
event_dependency_graph.py
Phase 3 Event Dependency Graph & Hierarchy Traversal
Each event owns its unique mini knowledge graph:
- Childbirth (EVT_CHILD_FIRST_BIRTH): Marriage Base (7th) -> 5th House -> 5th Lord -> Jupiter -> Putrakaraka -> Saptamsha D7 -> Dasha Trigger -> Transit Blessing
- Career (EVT_CAR_PROMOTION): Education Base (4th) -> Skill (5th) -> Current Job (6th) -> Income Gains (11th) -> Executive Authority (10th) -> Dasha Trigger -> Transit Luck
"""

from typing import Dict, List, Any

class EventDependencyGraph:
    """Models event-specific cross-event dependencies and hierarchy traversal."""

    DEPENDENCY_HIERARCHY = {
        "EVT_CHILD_FIRST_BIRTH": {
            "chain": ["Marriage Base (7th)", "Progeny Promise (5th House)", "5th Lord Strength", "Jupiter Karaka", "Putrakaraka (Jaimini)", "Saptamsha (D7)", "Dasha Trigger (5th Lord)", "Jupiter Transit Blessing (5th)"],
            "nodes_count": 8,
            "edges_count": 7
        },
        "EVT_CAR_PROMOTION": {
            "chain": ["Education Base (4th)", "Skill & Intellect (5th)", "Current Job (6th)", "Income Gains (11th)", "Executive Authority (10th)", "Dashamsha (D10)", "Dasha Trigger (10th Lord)", "Transit Luck (Jupiter/Saturn)"],
            "nodes_count": 8,
            "edges_count": 7
        },
        "EVT_MAR_TIMING": {
            "chain": ["Emotional Maturity (1st)", "Spouse Promise (7th)", "Family Wealth (2nd)", "Upapada Lagna (12th)", "Navamsha (D9)", "Jupiter Transit Aspect (7th)"],
            "nodes_count": 6,
            "edges_count": 5
        },
        "EVT_FOR_SETTLEMENT": {
            "chain": ["Birthland Anchor (4th)", "Long Travel Promise (9th)", "Foreign Land Residence (12th)", "Rahu Drive", "Chaturthamsha (D4)", "Dasha Trigger (12th Lord)"],
            "nodes_count": 6,
            "edges_count": 5
        }
    }

    @classmethod
    def get_dependency_traversal(cls, event_id: str) -> Dict[str, Any]:
        dep = cls.DEPENDENCY_HIERARCHY.get(event_id, cls.DEPENDENCY_HIERARCHY["EVT_CAR_PROMOTION"])
        return {
            "event_id": event_id,
            "dependency_chain_visual": " -> ".join(dep["chain"]),
            "dependency_nodes": dep["chain"],
            "nodes_count": dep["nodes_count"],
            "edges_count": dep["edges_count"]
        }
