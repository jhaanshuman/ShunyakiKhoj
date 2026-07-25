from .ashtakoota import calculate_ashtakoota
from .dashakoota import calculate_dashakoota
from .dosha_matching import check_doshas

def calculate_matching(boy_master_obj, girl_master_obj):
    """
    Orchestrator for matching logic. Returns unified compatibility analysis.
    """
    ashtakoota = calculate_ashtakoota(
        boy_master_obj.get('rashi'), 
        boy_master_obj.get('nakshatra'), 
        girl_master_obj.get('rashi'), 
        girl_master_obj.get('nakshatra')
    )
    
    dashakoota = calculate_dashakoota(
        boy_master_obj.get('nakshatra'), 
        girl_master_obj.get('nakshatra')
    )
    
    doshas = check_doshas(boy_master_obj, girl_master_obj)
    
    recommendation = "Average match. Proceed with caution."
    if ashtakoota['total_points'] > 18 and doshas['manglik']['status'] == "Match":
        recommendation = "Good match. Compatibility looks positive."
        
    return {
        "status": "success",
        "ashtakoota": ashtakoota,
        "dashakoota": dashakoota,
        "doshas": doshas,
        "recommendation": recommendation
    }
