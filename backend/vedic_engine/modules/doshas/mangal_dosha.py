# -*- coding: utf-8 -*-
"""
Mangal Dosha Engine v5.0.
Evaluates Manglik Dosha based on Mars position from Lagna, Moon, and Venus, plus 7 classical cancellations.
"""

def evaluate_mangal_dosha(master_obj: dict) -> dict:
    """Evaluates Manglik Dosha deterministically."""
    dosha_positions = [1, 2, 4, 7, 8, 12]

    planets = master_obj.get("planets", {})
    houses = master_obj.get("houses", {})
    dignity = master_obj.get("dignity", {})
    aspects = master_obj.get("planetary_aspects", [])

    mars_info = planets.get("Mars", {})
    moon_info = planets.get("Moon", {})
    venus_info = planets.get("Venus", {})

    mars_sign_idx = mars_info.get("sign_index", 0)
    moon_sign_idx = moon_info.get("sign_index", 0)
    venus_sign_idx = venus_info.get("sign_index", 0)
    asc_sign_idx = int(houses.get("ascendant_sidereal_lon", 0.0) / 30.0) % 12

    mars_house_lagna = ((mars_sign_idx - asc_sign_idx + 12) % 12) + 1
    mars_house_moon = ((mars_sign_idx - moon_sign_idx + 12) % 12) + 1
    mars_house_venus = ((mars_sign_idx - venus_sign_idx + 12) % 12) + 1

    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    mars_sign = SIGN_NAMES[mars_sign_idx]

    affected_houses = []
    if mars_house_lagna in dosha_positions: affected_houses.append(f"Lagna-{mars_house_lagna}th")
    if mars_house_moon in dosha_positions: affected_houses.append(f"Moon-{mars_house_moon}th")
    if mars_house_venus in dosha_positions: affected_houses.append(f"Venus-{mars_house_venus}th")

    is_manglik = len(affected_houses) > 0
    cancellation_reasons = []

    if is_manglik:
        if mars_sign in ["Aries", "Scorpio", "Capricorn"]:
            cancellation_reasons.append("Mars is in own or exalted sign.")

        # Jupiter aspect/conjunction
        jup_aspects = any(a.get("aspecting_planet") == "Jupiter" and a.get("target_planet") == "Mars" and a.get("is_effective", True) for a in aspects)
        jup_same_sign = planets.get("Jupiter", {}).get("sign_index") == mars_sign_idx
        if jup_aspects or jup_same_sign:
            cancellation_reasons.append("Jupiter aspects or conjoins Mars.")

        sat_aspects = any(a.get("aspecting_planet") == "Saturn" and a.get("target_planet") == "Mars" and a.get("is_effective", True) for a in aspects)
        if sat_aspects:
            cancellation_reasons.append("Saturn aspects Mars.")

        if mars_house_lagna == 2 and mars_sign in ["Gemini", "Virgo"]:
            cancellation_reasons.append("Mars in 2nd house in Gemini/Virgo.")
        if mars_house_lagna == 4 and mars_sign in ["Aries", "Scorpio"]:
            cancellation_reasons.append("Mars in 4th house in Aries/Scorpio.")
        if mars_house_lagna == 7 and mars_sign in ["Cancer", "Capricorn"]:
            cancellation_reasons.append("Mars in 7th house in Cancer/Capricorn.")
        if mars_house_lagna == 8 and mars_sign in ["Sagittarius", "Pisces"]:
            cancellation_reasons.append("Mars in 8th house in Sagittarius/Pisces.")
        if mars_house_lagna == 12 and mars_sign in ["Taurus", "Libra"]:
            cancellation_reasons.append("Mars in 12th house in Taurus/Libra.")

    is_cancelled = len(cancellation_reasons) > 0

    severity = "None"
    score = 0
    if is_manglik and not is_cancelled:
        if len(affected_houses) >= 3:
            severity = "High"
            score = 100
        elif len(affected_houses) == 2:
            severity = "Medium"
            score = 75
        else:
            severity = "Low"
            score = 50
    elif is_manglik and is_cancelled:
        severity = "Cancelled"
        score = 10

    return {
        "id": "DOSHA_MANGAL",
        "name": "Mangal Dosha (Manglik)",
        "is_present": is_manglik,
        "is_cancelled": is_cancelled,
        "severity": severity,
        "severity_score": score,
        "affected_houses": affected_houses,
        "affected_planets": ["Mars"],
        "cancellation_reasons": cancellation_reasons,
        "confidence": 98.0
    }
