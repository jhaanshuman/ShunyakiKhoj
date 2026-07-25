# -*- coding: utf-8 -*-
"""
Karakamsha Engine v5.0.
Calculates Karakamsha (D9 sign of Atmakaraka) and Swamsha (D1 sign of Atmakaraka).
"""

SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_karakamsha(planets: dict, ak_planet: str):
    """Calculate Karakamsha (D9 sign of Atmakaraka) and Swamsha (D1 sign of Atmakaraka)."""
    if ak_planet not in planets:
        return 'Aries', 'Aries'

    ak_data = planets[ak_planet]
    lon = ak_data.get('sidereal_lon', ak_data.get('lon', 0.0))

    # Swamsha: D1 sign name
    sign_idx = int((lon % 360.0) // 30)
    swamsha_sign = SIGN_NAMES[sign_idx % 12]

    # Karakamsha: D9 Navamsa sign name
    sign_lon = lon % 30.0
    part = int(sign_lon // (30.0 / 9.0))
    element = sign_idx % 4
    starts = [0, 9, 6, 3]  # Fire -> Aries, Earth -> Cap, Air -> Lib, Water -> Can
    d9_sign_idx = (starts[element] + part) % 12
    karakamsha_sign = SIGN_NAMES[d9_sign_idx]

    return karakamsha_sign, swamsha_sign

def analyze_karakamsha(planets: dict, karakamsha_sign: str, d9_positions: dict):
    """Analyze planets from Karakamsha in Navamsa."""
    analysis = {}
    return analysis
