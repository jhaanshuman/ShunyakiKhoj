# -*- coding: utf-8 -*-
"""
Ashtakavarga Engine: Computes BAV, SAV, Prastara, Reductions (Shodhana), and Pinda Strengths.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from .planets import SIGN_NAMES

# Classical Benefic Bindu Rules (house offsets from planet for BAV)
# Format: planet -> list of benefic houses from each contributing planet
ASHTAKAVARGA_RULES = {
    'Sun': {
        'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon': [3, 6, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [5, 6, 9, 11],
        'Venus': [6, 7, 12],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Asc': [3, 4, 6, 10, 11, 12]
    },
    'Moon': {
        'Sun': [3, 6, 7, 8, 10, 11],
        'Moon': [1, 3, 6, 7, 10, 11],
        'Mars': [2, 3, 5, 6, 9, 10, 11],
        'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
        'Jupiter': [1, 4, 7, 8, 10, 11, 12],
        'Venus': [3, 4, 5, 7, 9, 10, 11],
        'Saturn': [3, 5, 6, 11],
        'Asc': [3, 6, 10, 11]
    },
    'Mars': {
        'Sun': [3, 5, 6, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [3, 5, 6, 11],
        'Jupiter': [6, 10, 11, 12],
        'Venus': [6, 8, 11, 12],
        'Saturn': [1, 4, 7, 8, 9, 10, 11],
        'Asc': [1, 3, 6, 10, 11]
    },
    'Mercury': {
        'Sun': [5, 6, 9, 11, 12],
        'Moon': [2, 4, 6, 8, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [6, 8, 11, 12],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 11],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Asc': [1, 2, 4, 6, 8, 10, 11]
    },
    'Jupiter': {
        'Sun': [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Moon': [2, 5, 7, 9, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
        'Venus': [2, 5, 6, 9, 10, 11],
        'Saturn': [3, 5, 6, 12],
        'Asc': [1, 2, 4, 5, 6, 7, 9, 10, 11]
    },
    'Venus': {
        'Sun': [8, 11, 12],
        'Moon': [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Mars': [3, 5, 6, 9, 11, 12],
        'Mercury': [3, 5, 6, 9, 11],
        'Jupiter': [5, 8, 9, 10, 11],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn': [3, 4, 5, 8, 9, 10, 11],
        'Asc': [1, 2, 3, 4, 5, 8, 9, 11]
    },
    'Saturn': {
        'Sun': [1, 2, 4, 7, 8, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [3, 5, 6, 10, 11, 12],
        'Mercury': [6, 8, 9, 10, 11, 12],
        'Jupiter': [5, 6, 11, 12],
        'Venus': [6, 11, 12],
        'Saturn': [3, 5, 6, 11],
        'Asc': [1, 3, 4, 6, 10, 11]
    }
}

class AshtakavargaEngine:
    """Computes BAV, SAV, Reductions, and Pindas."""
    
    @classmethod
    def calculate_bav_and_sav(
        cls,
        planets_data: Dict[str, Any],
        asc_sid_lon: float
    ) -> Dict[str, Any]:
        """Compute Bhinna Ashtakavarga (BAV) and Sarvashtakavarga (SAV)."""
        asc_sign_idx = int((asc_sid_lon % 360.0) // 30)
        
        # Position index of each planet & Asc
        positions = {'Asc': asc_sign_idx}
        for p_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            p_obj = planets_data[p_name]
            p_lon = p_obj.sidereal_lon if hasattr(p_obj, 'sidereal_lon') else p_obj['sidereal_lon']
            positions[p_name] = int((p_lon % 360.0) // 30)
            
        bav_charts: Dict[str, List[int]] = {}
        sav_chart: List[int] = [0] * 12
        
        for main_p, rules in ASHTAKAVARGA_RULES.items():
            bav = [0] * 12
            for contributor, house_offsets in rules.items():
                c_sign = positions[contributor]
                for offset in house_offsets:
                    target_sign = (c_sign + offset - 1) % 12
                    bav[target_sign] += 1
            bav_charts[main_p] = bav
            for i in range(12):
                sav_chart[i] += bav[i]

        # Reductions (Trikona & Ekadhipatya Shodhana) for SAV
        trikona_sav = list(sav_chart)
        # Trikona reduction: 1-5-9, 2-6-10, 3-7-11, 4-8-12
        for tri in [[0, 4, 8], [1, 5, 9], [2, 6, 10], [3, 7, 11]]:
            min_v = min(trikona_sav[tri[0]], trikona_sav[tri[1]], trikona_sav[tri[2]])
            for idx in tri:
                trikona_sav[idx] -= min_v

        # Pinda calculations
        rashi_multipliers = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]
        graha_multipliers = {'Sun': 5, 'Moon': 5, 'Mars': 8, 'Mercury': 5, 'Jupiter': 10, 'Venus': 7, 'Saturn': 5}
        
        rashi_pinda = sum(trikona_sav[i] * rashi_multipliers[i] for i in range(12))
        graha_pinda = sum(trikona_sav[positions[p]] * mul for p, mul in graha_multipliers.items())
        shodhya_pinda = rashi_pinda + graha_pinda
        
        return {
            "bav": bav_charts,
            "sav": {
                "raw": sav_chart,
                "trikona_shodhana": trikona_sav,
                "total_bindus": sum(sav_chart)
            },
            "pinda": {
                "rashi_pinda": rashi_pinda,
                "graha_pinda": graha_pinda,
                "shodhya_pinda": shodhya_pinda
            }
        }
