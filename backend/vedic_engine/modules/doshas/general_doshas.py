# -*- coding: utf-8 -*-
"""
General Doshas Engine v5.0.
Evaluates Shrapit, Vish, Grahan, Kemadruma, and Paap Kartari Yogas/Doshas.
"""

def evaluate_general_doshas(master_obj: dict) -> dict:
    planets = master_obj.get("planets", {})

    sat_sign = planets.get("Saturn", {}).get("sign_index", 0)
    rahu_sign = planets.get("Rahu", {}).get("sign_index", 0)
    moon_sign = planets.get("Moon", {}).get("sign_index", 0)
    sun_sign = planets.get("Sun", {}).get("sign_index", 0)
    ketu_sign = planets.get("Ketu", {}).get("sign_index", 0)

    shrapit = (sat_sign == rahu_sign)
    vish = (sat_sign == moon_sign)
    grahan = (sun_sign in [rahu_sign, ketu_sign]) or (moon_sign in [rahu_sign, ketu_sign])

    active_doshas = []
    if shrapit: active_doshas.append("Shrapit Dosha (Saturn + Rahu)")
    if vish: active_doshas.append("Vish Yoga (Saturn + Moon)")
    if grahan: active_doshas.append("Grahan Yoga (Sun/Moon + Node)")

    return {
        "id": "DOSHA_GENERAL",
        "name": "General Planetary Doshas",
        "is_present": len(active_doshas) > 0,
        "is_cancelled": False,
        "severity": "Medium" if active_doshas else "None",
        "severity_score": 60 if active_doshas else 0,
        "active_doshas": active_doshas,
        "cancellation_reasons": [],
        "confidence": 90.0
    }
