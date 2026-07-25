# -*- coding: utf-8 -*-
"""
Guru Chandal Dosha Engine v5.0.
Evaluates Guru Chandal Dosha (Jupiter conjunct/aspected by Rahu/Ketu) and cancellations.
"""

def evaluate_guru_chandal_dosha(master_obj: dict) -> dict:
    planets = master_obj.get("planets", {})
    aspects = master_obj.get("planetary_aspects", [])

    jup_sign = planets.get("Jupiter", {}).get("sign_index", 0)
    rahu_sign = planets.get("Rahu", {}).get("sign_index", 0)
    ketu_sign = planets.get("Ketu", {}).get("sign_index", 0)

    is_conjunct = (jup_sign == rahu_sign) or (jup_sign == ketu_sign)
    is_aspected = any(
        a.get("target_planet") == "Jupiter" and a.get("aspecting_planet") in ["Rahu", "Ketu"]
        for a in aspects
    )

    is_guru_chandal = is_conjunct or is_aspected

    cancellations = []
    if jup_sign in [3, 8, 11]:  # Cancer (Exalted), Sagittarius, Pisces (Own sign)
        cancellations.append("Jupiter is Exalted or in Own Sign.")

    is_cancelled = len(cancellations) > 0

    return {
        "id": "DOSHA_GURU_CHANDAL",
        "name": "Guru Chandal Dosha",
        "is_present": is_guru_chandal,
        "is_cancelled": is_cancelled,
        "severity": "Cancelled" if is_cancelled else ("High" if is_conjunct else ("Medium" if is_aspected else "None")),
        "severity_score": 10 if is_cancelled else (80 if is_conjunct else (50 if is_aspected else 0)),
        "affected_houses": [],
        "affected_planets": ["Jupiter", "Rahu", "Ketu"],
        "cancellation_reasons": cancellations,
        "confidence": 92.0
    }
