from typing import List, Dict, Any
from .yoga_base import YogaResult, YogaEvaluator

class SolarYogaEvaluator(YogaEvaluator):
    def evaluate(self, master_obj: Dict[str, Any]) -> List[YogaResult]:
        yogas = []
        
        # Vesi Yoga
        is_active = master_obj.get("vesi_yoga", False)
        if is_active:
            yogas.append(YogaResult(
                id="sy_001",
                name="Vesi Yoga",
                sanskrit="वेशि योग",
                category="Solar Yoga",
                source_text="BPHS",
                chapter="37",
                verse="4",
                is_active=is_active,
                strength=75.0,
                confidence=100.0,
                rules_matched=["Planet(s) other than Moon in 2nd from Sun"],
                affected_domains=["Fame", "Status"],
                evidence_chain=["Venus is in 2nd from Sun"]
            ))
            
        return yogas
