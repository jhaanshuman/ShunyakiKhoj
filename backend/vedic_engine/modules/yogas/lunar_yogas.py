from typing import List, Dict, Any
from .yoga_base import YogaResult, YogaEvaluator

class LunarYogaEvaluator(YogaEvaluator):
    def evaluate(self, master_obj: Dict[str, Any]) -> List[YogaResult]:
        yogas = []
        
        # Sunapha Yoga
        is_active = master_obj.get("sunapha_yoga", False)
        if is_active:
            yogas.append(YogaResult(
                id="ly_001",
                name="Sunapha Yoga",
                sanskrit="सुनफा योग",
                category="Lunar Yoga",
                source_text="BPHS",
                chapter="37",
                verse="1-2",
                is_active=is_active,
                strength=70.0,
                confidence=100.0,
                rules_matched=["Planet(s) other than Sun in 2nd from Moon"],
                affected_domains=["Wealth", "Intelligence"],
                evidence_chain=["Jupiter is in 2nd from Moon"]
            ))
            
        # Anapha, Durudhara, Kemadruma, Gajakesari
        return yogas
