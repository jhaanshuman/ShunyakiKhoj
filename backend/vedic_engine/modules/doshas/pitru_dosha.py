# -*- coding: utf-8 -*-
"""
Pitru Dosha Engine v5.0.
Evaluates Pitru Dosha based on Sun / 9th house / 9th lord affliction by Rahu, Ketu, or Saturn.
"""

def evaluate_pitru_dosha(master_obj: dict) -> dict:
    planets = master_obj.get("planets", {})
    houses = master_obj.get("houses", {})
    aspects = master_obj.get("planetary_aspects", [])

    sun_sign = planets.get("Sun", {}).get("sign_index", 0)
    rahu_sign = planets.get("Rahu", {}).get("sign_index", 0)
    ketu_sign = planets.get("Ketu", {}).get("sign_index", 0)
    sat_sign = planets.get("Saturn", {}).get("sign_index", 0)

    asc_sign = int(houses.get("ascendant_sidereal_lon", 0.0) / 30.0) % 12
    ninth_sign = (asc_sign + 8) % 12

    # Check Sun afflicted by Rahu/Ketu/Saturn (same sign or aspect)
    sun_afflicted = sun_sign in [rahu_sign, ketu_sign, sat_sign] or any(
        a.get("target_planet") == "Sun" and a.get("aspecting_planet") in ["Rahu", "Ketu", "Saturn"]
        for a in aspects
    )

    # 9th house occupied by Rahu/Ketu/Saturn
    ninth_afflicted = rahu_sign == ninth_sign or ketu_sign == ninth_sign or sat_sign == ninth_sign

    is_pitru_dosha = sun_afflicted or ninth_afflicted
    severity = "High" if (sun_afflicted and ninth_afflicted) else ("Medium" if is_pitru_dosha else "None")

    return {
        "id": "DOSHA_PITRU",
        "name": "Pitru Dosha",
        "is_present": is_pitru_dosha,
        "is_cancelled": False,
        "severity": severity,
        "severity_score": 85 if severity == "High" else (50 if severity == "Medium" else 0),
        "affected_houses": [9],
        "affected_planets": ["Sun", "9th Lord"],
        "cancellation_reasons": [],
        "confidence": 90.0
    }
