from typing import Dict, Any, List
from .dasha_base import DashaPeriod
from .vimshottari import calculate_vimshottari
from .yogini import calculate_yogini
from .ashtottari import calculate_ashtottari
from .kalachakra import calculate_kalachakra
from .chara import calculate_chara
from .sthira import calculate_sthira
from .narayana import calculate_narayana
from .shoola import calculate_shoola
from .mandooka import calculate_mandooka
from .panchottari import calculate_panchottari
from .dwadashottari import calculate_dwadashottari
from .shatabdika import calculate_shatabdika
from .chaturashiti_sama import calculate_chaturashiti_sama
from .dwisaptati_sama import calculate_dwisaptati_sama
from .shodashottari import calculate_shodashottari
from .tara import calculate_tara
from .naisargika import calculate_naisargika
from .lagna_kendradi import calculate_lagna_kendradi
from .sudarshana_chakra import calculate_sudarshana_chakra

def calculate_all_dashas(master_obj: Any, requested_dashas: List[str] = None) -> Dict[str, Any]:
    if requested_dashas is None:
        requested_dashas = ['ALL']
        
    result = {}
    
    dashas_map = {
        'vimshottari': calculate_vimshottari,
        'yogini': calculate_yogini,
        'ashtottari': calculate_ashtottari,
        'kalachakra': calculate_kalachakra,
        'chara': calculate_chara,
        'sthira': calculate_sthira,
        'narayana': calculate_narayana,
        'shoola': calculate_shoola,
        'mandooka': calculate_mandooka,
        'panchottari': calculate_panchottari,
        'dwadashottari': calculate_dwadashottari,
        'shatabdika': calculate_shatabdika,
        'chaturashiti_sama': calculate_chaturashiti_sama,
        'dwisaptati_sama': calculate_dwisaptati_sama,
        'shodashottari': calculate_shodashottari,
        'tara': calculate_tara,
        'naisargika': calculate_naisargika,
        'lagna_kendradi': calculate_lagna_kendradi,
        'sudarshana_chakra': calculate_sudarshana_chakra
    }
    
    for dasha_name, func in dashas_map.items():
        if 'ALL' in requested_dashas or dasha_name in requested_dashas:
            periods = func(master_obj)
            result[dasha_name] = [p.to_dict() for p in periods]
            
    return result
