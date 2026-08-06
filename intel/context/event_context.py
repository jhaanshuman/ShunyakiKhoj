# -*- coding: utf-8 -*-
"""
event_context.py
Sprint 5 Immutable EventContext Container with Unique Event Fingerprints.
Defines rule_namespace, citation_namespace, required_varga, required_houses, and karakas.
Zero shared state, zero global variables, zero template leakage.
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class EventContext:
    event_id: str
    event_name: str
    domain_code: str
    required_houses: List[int]
    required_karakas: List[str]
    varga_chart: str
    rule_namespace: str
    citation_namespace: str
    rules: List[Dict[str, Any]]
    citations: List[Dict[str, Any]]
    remedies: List[Dict[str, Any]]
    expected_indicators: List[str]

    def get_fingerprint(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "domain_code": self.domain_code,
            "required_varga": self.varga_chart,
            "karakas": self.required_karakas,
            "houses": self.required_houses,
            "rule_namespace": self.rule_namespace,
            "citation_namespace": self.citation_namespace
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "domain_code": self.domain_code,
            "required_houses": self.required_houses,
            "required_karakas": self.required_karakas,
            "varga_chart": self.varga_chart,
            "rule_namespace": self.rule_namespace,
            "citation_namespace": self.citation_namespace,
            "rules_count": len(self.rules),
            "citations_count": len(self.citations),
            "remedies_count": len(self.remedies),
            "expected_indicators": self.expected_indicators,
            "fingerprint": self.get_fingerprint()
        }
