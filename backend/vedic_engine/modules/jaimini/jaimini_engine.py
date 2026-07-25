# -*- coding: utf-8 -*-
"""
Jaimini Engine Orchestrator v5.0.
Computes Chara Karakas, Karakamsha, Swamsha, Arudha Padas, Jaimini Aspects, and Jaimini Raj Yogas.
"""

from .chara_karakas import calculate_chara_karakas
from .karakamsha import get_karakamsha, analyze_karakamsha
from .arudhas import calculate_arudha_padas
from .aspects import get_jaimini_aspects
from .raj_yogas import calculate_raj_yogas

SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def calculate_jaimini(master_obj: dict) -> dict:
    """Orchestrator for complete Jaimini Analysis."""
    planets = master_obj.get('planets', {})
    houses_dict = master_obj.get('houses', {})

    asc_lon = houses_dict.get('ascendant_sidereal_lon', 0.0) if isinstance(houses_dict, dict) else 0.0
    asc_sign_idx = int(asc_lon / 30.0) % 12

    # Map 12 houses to their sign indices (1-indexed sign number 1..12)
    house_signs = [((asc_sign_idx + h - 1) % 12) + 1 for h in range(1, 13)]

    # Map house sign to lord's sign
    lords_positions = {}
    for s_idx in range(12):
        s_num = s_idx + 1
        lord_name = SIGN_LORDS[s_idx]
        lord_p = planets.get(lord_name, {})
        lord_sign_idx = lord_p.get('sign_index', 0)
        lords_positions[s_num] = lord_sign_idx + 1

    chara_karakas = calculate_chara_karakas(planets, use_eight=False)

    ak = chara_karakas.get('AK', 'Sun')
    karakamsha_sign, swamsha_sign = get_karakamsha(planets, ak)

    arudhas = calculate_arudha_padas(house_signs, lords_positions)

    planet_signs = {p: data.get('sign_name', SIGN_NAMES[data.get('sign_index', 0)]) for p, data in planets.items()}
    raj_yogas = calculate_raj_yogas(chara_karakas, planet_signs)

    return {
        'chara_karakas': chara_karakas,
        'karakamsha_sign': karakamsha_sign,
        'swamsha_sign': swamsha_sign,
        'arudha_padas': arudhas,
        'raj_yogas': raj_yogas,
        'aspects': get_jaimini_aspects()
    }
