from typing import List, Dict, Any
from .yoga_base import YogaResult, YogaEvaluator

class ParivartanaYogaEvaluator(YogaEvaluator):
    def evaluate(self, master_obj: Dict[str, Any]) -> List[YogaResult]:
        yogas = []
        
        # Maha Yoga
        is_active = master_obj.get("maha_yoga", False)
        if is_active:
            yogas.append(YogaResult(
                id="py_001",
                name="Maha Yoga",
                sanskrit="महा योग",
                category="Parivartana Yoga",
                source_text="Phaladeepika",
                chapter="6",
                verse="32",
                is_active=is_active,
                strength=95.0,
                confidence=100.0,
                rules_matched=["Exchange between 1st and 9th lord"],
                affected_domains=["Overall Success", "Luck"],
                evidence_chain=["Lagnesh in 9th and 9th lord in 1st"]
            ))
            
        # Dainya Yoga, Khala Yoga
        return yogas
