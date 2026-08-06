# -*- coding: utf-8 -*-
"""
event_compiler.py
Astrological Declarative Compiler
Compiles declarative JSON/YAML event specifications into executable reasoning workflows automatically.
Instead of hard-coding Python logic per event, the engine reads structured event specs.
"""

from typing import Dict, List, Any
import os
import json

class AstrologicalEventCompiler:
    """Compiles declarative event specifications into executable reasoning objects."""

    def __init__(self, specs_dir: str = None):
        if specs_dir is None:
            specs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specs")
        self.specs_dir = specs_dir
        self.compiled_events: Dict[str, Dict[str, Any]] = {}
        self._compile_all_specs()

    def _compile_all_specs(self):
        if not os.path.exists(self.specs_dir):
            return

        for fname in os.listdir(self.specs_dir):
            if fname.endswith(".json"):
                fpath = os.path.join(self.specs_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    spec = json.load(f)

                event_id = spec.get("event_id")
                domain_code = spec.get("domain_code", "GENERAL")
                rule_ns = spec.get("rule_namespace", domain_code.split("_")[0])
                citation_ns = spec.get("citation_namespace", domain_code.split("_")[0])

                compiled_obj = {
                    "event_id": event_id,
                    "event_name": spec.get("event_name"),
                    "domain_code": domain_code,
                    "rule_namespace": rule_ns,
                    "citation_namespace": citation_ns,
                    "required_houses": spec.get("required_indicators", {}).get("houses", []),
                    "required_karakas": spec.get("required_indicators", {}).get("karakas", []),
                    "varga_chart": spec.get("required_indicators", {}).get("varga_chart", "D1"),
                    "timing_dashas": spec.get("timing_rules", {}).get("dashas", []),
                    "timing_transits": spec.get("timing_rules", {}).get("transits", []),
                    "negative_factors": spec.get("negative_factors", []),
                    "cancellation_rules": spec.get("cancellation_rules", []),
                    "classical_citations": spec.get("classical_citations", []),
                    "remedies": spec.get("remedies", []),
                    "compiled": True
                }

                self.compiled_events[event_id] = compiled_obj

    def get_compiled_event(self, event_id: str) -> Dict[str, Any]:
        if event_id in self.compiled_events:
            return self.compiled_events[event_id]

        # Search fallback by domain code
        for spec in self.compiled_events.values():
            if spec.get("domain_code") == event_id or spec.get("rule_namespace") in event_id:
                return spec

        return list(self.compiled_events.values())[0] if self.compiled_events else {}
