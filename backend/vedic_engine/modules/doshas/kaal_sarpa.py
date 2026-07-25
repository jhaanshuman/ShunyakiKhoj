# -*- coding: utf-8 -*-
"""
Kaal Sarpa & Kala Amrita Dosha Engine v5.0.
Evaluates all 12 variants of Kaal Sarpa Dosha and cancellations.
"""

def evaluate_kaal_sarpa_dosha(master_obj: dict) -> dict:
    planets = master_obj.get("planets", {})
    houses = master_obj.get("houses", {})

    rahu_lon = planets.get("Rahu", {}).get("sidereal_lon", 0.0)
    ketu_lon = planets.get("Ketu", {}).get("sidereal_lon", 180.0)

    planet_names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    planet_lons = [planets.get(p, {}).get("sidereal_lon", 0.0) for p in planet_names]

    # Check if all 7 planets are hemmed between Rahu and Ketu
    def is_between(lon, start, end):
        if start < end:
            return start <= lon <= end
        else:
            return lon >= start or lon <= end

    side1 = all(is_between(l, rahu_lon, ketu_lon) for l in planet_lons)
    side2 = all(is_between(l, ketu_lon, rahu_lon) for l in planet_lons)

    is_kaal_sarpa = side1 or side2
    is_kala_amrita = side2

    rahu_house = planets.get("Rahu", {}).get("house", 1)
    if "house" not in planets.get("Rahu", {}):
        rahu_sign = planets.get("Rahu", {}).get("sign_index", 0)
        asc_sign = int(houses.get("ascendant_sidereal_lon", 0.0) / 30.0) % 12
        rahu_house = ((rahu_sign - asc_sign + 12) % 12) + 1

    VARIANTS = {
        1: "Ananta Kaal Sarpa (1st-7th)",
        2: "Kulika Kaal Sarpa (2nd-8th)",
        3: "Vasuki Kaal Sarpa (3rd-9th)",
        4: "Shankhapala Kaal Sarpa (4th-10th)",
        5: "Padma Kaal Sarpa (5th-11th)",
        6: "Mahapadma Kaal Sarpa (6th-12th)",
        7: "Takshaka Kaal Sarpa (7th-1st)",
        8: "Karkotaka Kaal Sarpa (8th-2nd)",
        9: "Shankhanaad Kaal Sarpa (9th-3rd)",
        10: "Pataka Kaal Sarpa (10th-4th)",
        11: "Vishakta Kaal Sarpa (11th-5th)",
        12: "Sheshanaga Kaal Sarpa (12th-6th)"
    }

    variant_name = VARIANTS.get(rahu_house, "Kaal Sarpa Dosha")
    if is_kala_amrita:
        variant_name = variant_name.replace("Kaal Sarpa", "Kala Amrita")

    cancellations = []
    # Check if Jupiter or Lagna lord is strong
    jup_dignity = master_obj.get("dignity", {}).get("Jupiter", {}).get("dignity_state", "")
    if "Exalted" in jup_dignity or "Own" in jup_dignity:
        cancellations.append("Jupiter is Exalted or in Own Sign.")

    is_cancelled = len(cancellations) > 0

    return {
        "id": "DOSHA_KAAL_SARPA",
        "name": variant_name,
        "is_present": is_kaal_sarpa,
        "is_cancelled": is_cancelled,
        "severity": "High" if (is_kaal_sarpa and not is_cancelled) else ("Cancelled" if is_cancelled else "None"),
        "severity_score": 90 if (is_kaal_sarpa and not is_cancelled) else (10 if is_cancelled else 0),
        "affected_houses": [rahu_house, ((rahu_house + 5) % 12) + 1],
        "affected_planets": ["Rahu", "Ketu"],
        "cancellation_reasons": cancellations,
        "confidence": 95.0
    }
