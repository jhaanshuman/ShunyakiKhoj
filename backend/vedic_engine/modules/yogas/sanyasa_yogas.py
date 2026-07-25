from typing import List, Dict, Any
from .yoga_base import YogaResult, YogaEvaluator

class SanyasaYogaEvaluator(YogaEvaluator):
    def evaluate(self, master_obj: Dict[str, Any]) -> List[YogaResult]:
        yogas = []
        
        # Sanyasa Yoga
        is_active = master_obj.get("sanyasa_yoga", False)
        if is_active:
            yogas.append(YogaResult(
                id="sanyy_001",
                name="Pravrajya Yoga",
                sanskrit="प्रव्रज्या योग",
                category="Sanyasa Yoga",
                source_text="Phaladeepika",
                chapter="27",
                verse="2",
                is_active=is_active,
                strength=85.0,
                confidence=95.0,
                rules_matched=["4 or more planets in a single house"],
                affected_domains=["Spirituality", "Renunciation"],
                evidence_chain=["Sun, Moon, Mercury, and Venus in 9th house"]
            ))
            
        return yogas
