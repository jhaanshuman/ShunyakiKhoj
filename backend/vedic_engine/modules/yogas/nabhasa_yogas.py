from typing import List, Dict, Any
from .yoga_base import YogaResult, YogaEvaluator

class NabhasaYogaEvaluator(YogaEvaluator):
    def evaluate(self, master_obj: Dict[str, Any]) -> List[YogaResult]:
        yogas = []
        
        # Rajju Yoga
        is_active = master_obj.get("rajju_yoga", False)
        if is_active:
            yogas.append(YogaResult(
                id="ny_001",
                name="Rajju Yoga",
                sanskrit="रज्जु योग",
                category="Nabhasa Yoga",
                source_text="BPHS",
                chapter="35",
                verse="1-2",
                is_active=is_active,
                strength=60.0,
                confidence=100.0,
                rules_matched=["All planets in movable signs"],
                affected_domains=["Travel", "Adaptability"],
                evidence_chain=["All 7 planets located in signs 1, 4, 7, 10"]
            ))
            
        return yogas
