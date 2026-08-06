# -*- coding: utf-8 -*-
"""
event_ontology.py
Deliverable 2: Event Ontology
Defines every life event as a structured object containing Primary/Secondary/Supporting indicators,
Timing indicators, Cancellation rules, Positive/Negative factors, Dependencies, and Remedy rules.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class EventSpecification:
    event_id: str
    event_name: str
    domain_code: str
    primary_houses: List[int]
    primary_karakas: List[str]
    secondary_houses: List[int]
    divisional_chart: str  # e.g. D9 for Marriage, D10 for Career
    upapada_lagna_relevant: bool = False
    darakaraka_relevant: bool = False
    timing_dashas: List[str] = field(default_factory=list)
    positive_indicators: List[str] = field(default_factory=list)
    negative_indicators: List[str] = field(default_factory=list)
    cancellation_rules: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

class EventOntology:
    """Master event ontology catalog for structured astrological events."""

    EVENTS: Dict[str, EventSpecification] = {
        "MARRIAGE_TIMING": EventSpecification(
            event_id="EVT_MAR_01",
            event_name="Marriage Timing & Union",
            domain_code="MARRIAGE",
            primary_houses=[7, 2, 11],
            primary_karakas=["Venus", "Jupiter"],
            secondary_houses=[1, 5, 8],
            divisional_chart="D9",
            upapada_lagna_relevant=True,
            darakaraka_relevant=True,
            timing_dashas=["7th Lord", "Venus", "Jupiter", "UL Lord", "Darakaraka"],
            positive_indicators=[
                "7th Lord placed in Kendra or Trikona",
                "Jupiter transit aspecting 7th house or 7th lord",
                "Venus in strong dignity in D1 and D9",
                "Upapada Lagna (UL) benefic aspected"
            ],
            negative_indicators=[
                "Saturn or Rahu afflicting 7th house or 7th lord",
                "7th Lord combust or in 6th/8th/12th house",
                "Kuja Dosha / Mangal Dosha without cancellation",
                "Upapada Lagna in 8th or 12th from Lagna"
            ],
            cancellation_rules=[
                "Jupiter aspecting 7th house neutralizes Saturn/Rahu afflictions",
                "Neecha Bhanga of 7th lord converts delay into lasting marital wealth"
            ],
            dependencies=["Natal Promise (7th House/Venus)", "Mahadasha Alignment", "Jupiter/Saturn Double Transit"]
        ),
        "CAREER_PROMOTION": EventSpecification(
            event_id="EVT_CAR_01",
            event_name="Career Promotion & Professional Rise",
            domain_code="CAREER",
            primary_houses=[10, 6, 11],
            primary_karakas=["Sun", "Saturn", "Mercury"],
            secondary_houses=[1, 2, 9],
            divisional_chart="D10",
            upapada_lagna_relevant=False,
            darakaraka_relevant=False,
            timing_dashas=["10th Lord", "6th Lord", "Sun", "Saturn"],
            positive_indicators=[
                "10th Lord conjunct 9th Lord (Dharma-Karma Adhipati Yoga)",
                "Sun or Saturn transiting 10th or 11th house with high Ashtakvarga bindus (≥30)",
                "Strong D10 Dashamsha Lagna and 10th lord",
                "Mahadasha of functional benefic or 10th/11th lord"
            ],
            negative_indicators=[
                "Saturn transit over 10th house during weak Ashtakvarga",
                "10th Lord in 8th house during Antardasha",
                "Rahu creating Guru Chandal or Eclipse on 10th house"
            ],
            cancellation_rules=[
                "Benefic Jupiter transit over 10th house overrides minor Dasha afflictions"
            ],
            dependencies=["Natal Promise (10th House/Sun)", "D10 Dashamsha Dignities", "10th/11th Dasha Active"]
        ),
        "FOREIGN_SETTLEMENT": EventSpecification(
            event_id="EVT_FOR_01",
            event_name="Foreign Settlement & Overseas PR",
            domain_code="FOREIGN",
            primary_houses=[9, 12, 7],
            primary_karakas=["Rahu", "Saturn"],
            secondary_houses=[3, 4],
            divisional_chart="D4",
            timing_dashas=["12th Lord", "9th Lord", "Rahu"],
            positive_indicators=[
                "12th Lord in 9th house or 9th Lord in 12th house (Parivartana)",
                "Rahu in 1st, 9th, or 12th house",
                "4th Lord in 12th house (moving away from birthplace)"
            ],
            negative_indicators=[
                "Strong 4th house and 4th lord keeping native anchored to home land"
            ],
            cancellation_rules=[],
            dependencies=["12th/9th House Influence", "Rahu Mahadasha/Antardasha"]
        )
    }

    @classmethod
    def get_event_spec(cls, event_key: str) -> EventSpecification:
        return cls.EVENTS.get(event_key, cls.EVENTS["CAREER_PROMOTION"])
