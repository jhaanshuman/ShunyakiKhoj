from typing import List, Dict, Any
from .yoga_base import YogaResult
from .raja_yogas import RajaYogaEvaluator
from .dhana_yogas import DhanaYogaEvaluator
from .lunar_yogas import LunarYogaEvaluator
from .solar_yogas import SolarYogaEvaluator
from .nabhasa_yogas import NabhasaYogaEvaluator
from .arishta_yogas import ArishtaYogaEvaluator
from .sanyasa_yogas import SanyasaYogaEvaluator
from .jaimini_yogas import JaiminiYogaEvaluator
from .parivartana_yogas import ParivartanaYogaEvaluator

def evaluate_all_300_yogas(master_obj: Dict[str, Any]) -> Dict[str, Any]:
    evaluators = [
        RajaYogaEvaluator(),
        DhanaYogaEvaluator(),
        LunarYogaEvaluator(),
        SolarYogaEvaluator(),
        NabhasaYogaEvaluator(),
        ArishtaYogaEvaluator(),
        SanyasaYogaEvaluator(),
        JaiminiYogaEvaluator(),
        ParivartanaYogaEvaluator()
    ]
    
    all_active_yogas: List[YogaResult] = []
    
    for evaluator in evaluators:
        yogas = evaluator.evaluate(master_obj)
        all_active_yogas.extend(yogas)
        
    # Sort top yogas by strength
    sorted_yogas = sorted(all_active_yogas, key=lambda x: x.strength, reverse=True)
    
    category_counts = {}
    for yoga in sorted_yogas:
        category_counts[yoga.category] = category_counts.get(yoga.category, 0) + 1
        
    return {
        "total_active": len(sorted_yogas),
        "categories_breakdown": category_counts,
        "yogas": [vars(y) for y in sorted_yogas]
    }
