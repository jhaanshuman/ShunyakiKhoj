from .mangal_dosha import evaluate_mangal_dosha
from .kaal_sarpa import evaluate_kaal_sarpa_dosha
from .pitru_dosha import evaluate_pitru_dosha
from .guru_chandal import evaluate_guru_chandal_dosha
from .marriage_doshas import evaluate_marriage_doshas
from .general_doshas import evaluate_general_doshas

def evaluate_all_doshas(master_obj):
    all_doshas = []
    
    all_doshas.append(evaluate_mangal_dosha(master_obj))
    all_doshas.append(evaluate_kaal_sarpa_dosha(master_obj))
    all_doshas.append(evaluate_pitru_dosha(master_obj))
    all_doshas.append(evaluate_guru_chandal_dosha(master_obj))
    
    all_doshas.append(evaluate_marriage_doshas(master_obj))
    all_doshas.append(evaluate_general_doshas(master_obj))
    
    # Filter valid doshas
    active_doshas = [d for d in all_doshas if d.get("severity", "None") != "None" or d.get("is_cancelled", False)]
    
    severe_count = sum(1 for d in active_doshas if d.get("severity") == "High")
    cancelled_count = sum(1 for d in active_doshas if d.get("is_cancelled"))
    
    return {
        "total_doshas_found": len(active_doshas),
        "severe_doshas_count": severe_count,
        "cancelled_doshas_count": cancelled_count,
        "doshas": active_doshas,
        "confidence": 0.95
    }
