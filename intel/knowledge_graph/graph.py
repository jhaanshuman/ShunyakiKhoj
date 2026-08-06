# -*- coding: utf-8 -*-
"""
graph.py
Deliverable 3: Astrological Knowledge Graph
Represents astrological reasoning as a directional network graph:
Event -> depends_on -> House -> depends_on -> Planet -> modified_by -> Dasha -> modified_by -> Transit
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class GraphEdge:
    source: str
    target: str
    relation_type: str  # depends_on, modified_by, cancels, strengthens, triggers
    weight: float = 1.0

class AstrologicalKnowledgeGraph:
    """Directional Knowledge Graph representing astrological dependencies."""

    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[GraphEdge] = []
        self._build_default_graph()

    def _build_default_graph(self):
        # Marriage Event Chain
        self.add_node("Marriage_Event", "EVENT", "Marriage & Union")
        self.add_node("House_7", "HOUSE", "7th House of Spouse & Marriage")
        self.add_node("House_7_Lord", "PLANET", "Lord of the 7th House")
        self.add_node("Venus_Karaka", "PLANET", "Venus (Naisargika Karaka for Marriage)")
        self.add_node("Navamsha_D9", "VARGA", "Navamsha D9 Chart")
        self.add_node("Upapada_Lagna", "PADA", "Upapada Lagna (UL)")
        self.add_node("Darakaraka", "JAIMINI", "Jaimini Darakaraka Planet")
        self.add_node("Saturn_Influence", "MALEFIC", "Saturn Aspect / Delay Factor")
        self.add_node("Jupiter_Transit", "TRANSIT", "Jupiter Transit Blessing")
        self.add_node("Mahadasha_System", "DASHA", "Active Vimshottari Mahadasha")

        self.add_edge("Marriage_Event", "House_7", "depends_on", 0.9)
        self.add_edge("House_7", "House_7_Lord", "depends_on", 0.85)
        self.add_edge("Marriage_Event", "Venus_Karaka", "depends_on", 0.8)
        self.add_edge("Marriage_Event", "Navamsha_D9", "depends_on", 0.85)
        self.add_edge("Marriage_Event", "Upapada_Lagna", "depends_on", 0.75)
        self.add_edge("Marriage_Event", "Darakaraka", "depends_on", 0.7)

        self.add_edge("House_7", "Saturn_Influence", "modified_by", -0.4)
        self.add_edge("Marriage_Event", "Jupiter_Transit", "triggers", 0.9)
        self.add_edge("Marriage_Event", "Mahadasha_System", "modified_by", 0.95)

        # Career Event Chain
        self.add_node("Career_Promotion", "EVENT", "Career Rise & Promotion")
        self.add_node("House_10", "HOUSE", "10th House of Career & Apex Status")
        self.add_node("House_10_Lord", "PLANET", "Lord of the 10th House")
        self.add_node("Sun_Karaka", "PLANET", "Sun (Karaka of Government & Authority)")
        self.add_node("Dashamsha_D10", "VARGA", "Dashamsha D10 Chart")

        self.add_edge("Career_Promotion", "House_10", "depends_on", 0.95)
        self.add_edge("House_10", "House_10_Lord", "depends_on", 0.9)
        self.add_edge("Career_Promotion", "Sun_Karaka", "depends_on", 0.8)
        self.add_edge("Career_Promotion", "Dashamsha_D10", "depends_on", 0.85)

    def add_node(self, node_id: str, node_type: str, label: str):
        self.nodes[node_id] = {"id": node_id, "type": node_type, "label": label}

    def add_edge(self, source: str, target: str, relation: str, weight: float = 1.0):
        self.edges.append(GraphEdge(source, target, relation, weight))

    def get_event_dependency_chain(self, event_node: str) -> List[Dict[str, Any]]:
        chain = []
        for edge in self.edges:
            if edge.source == event_node:
                chain.append({
                    "target_node": edge.target,
                    "target_info": self.nodes.get(edge.target, {}),
                    "relation": edge.relation_type,
                    "weight": edge.weight
                })
        return chain
