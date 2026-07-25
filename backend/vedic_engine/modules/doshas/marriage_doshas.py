# -*- coding: utf-8 -*-
"""
Marriage Compatibility Doshas v5.0.
Structural evaluation of single-chart marriage warning indicators.
"""

def evaluate_marriage_doshas(master_obj: dict) -> dict:
    planets = master_obj.get("planets", {})
    houses = master_obj.get("houses", {})

    asc_sign = int(houses.get("ascendant_sidereal_lon", 0.0) / 30.0) % 12
    seventh_sign = (asc_sign + 6) % 12
    eighth_sign = (asc_sign + 7) % 12

    venus_sign = planets.get("Venus", {}).get("sign_index", 0)

    # Malefics in 7th/8th house
    malefics = ["Mars", "Saturn", "Rahu", "Ketu", "Sun"]
    malefics_in_7th = [p for p in malefics if planets.get(p, {}).get("sign_index") == seventh_sign]
    malefics_in_8th = [p for p in malefics if planets.get(p, {}).get("sign_index") == eighth_sign]

    is_afflicted = len(malefics_in_7th) > 0 or len(malefics_in_8th) > 0

    return {
        "id": "DOSHA_MARRIAGE",
        "name": "Marriage Compatibility Indicators",
        "is_present": is_afflicted,
        "is_cancelled": False,
        "severity": "High" if (len(malefics_in_7th) + len(malefics_in_8th) >= 2) else ("Medium" if is_afflicted else "None"),
        "severity_score": 75 if is_afflicted else 0,
        "malefics_in_7th_house": malefics_in_7th,
        "malefics_in_8th_house": malefics_in_8th,
        "confidence": 90.0
    }
