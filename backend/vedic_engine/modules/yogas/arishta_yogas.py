from typing import List, Dict, Any
from .yoga_base import YogaResult, YogaEvaluator

class ArishtaYogaEvaluator(YogaEvaluator):
    def evaluate(self, master_obj: Dict[str, Any]) -> List[YogaResult]:
        yogas = []
        
        # Balarishta
        is_active = master_obj.get("balarishta", False)
        if is_active:
            yogas.append(YogaResult(
                id="ay_001",
                name="Balarishta",
                sanskrit="बालारिष्ट",
                category="Arishta Yoga",
                source_text="BPHS",
                chapter="10",
                verse="1",
                is_active=is_active,
                strength=80.0,
                confidence=95.0,
                rules_matched=["Moon in 6th/8th/12th with malefic aspect"],
                affected_domains=["Health", "Childhood"],
                evidence_chain=["Moon in 8th house afflicted by Saturn"]
            ))
            
        return yogas
