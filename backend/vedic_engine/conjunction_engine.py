# -*- coding: utf-8 -*-
"""
Conjunction, Planetary War (Graha Yuddha), and Combustion Engine v2.0.
Detects same-sign conjunctions with orb classification, planetary wars,
cazimi/combustion severity with planet-specific orbs, and stellium clusters.
New: 5-tier conjunction classification, is_effective filter, corrected war winner logic.
"""

class ConjunctionEngine:
    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    # Classical planet-specific combustion orbs (BPHS)
    COMBUSTION_ORBS = {
        'Moon':    {'cazimi': 0.2833, 'severe': 12.0,  'moderate': 20.0, 'mild': 20.0},  # Moon: within 12° combust
        'Mars':    {'cazimi': 0.2833, 'severe': 3.0,   'moderate': 10.0, 'mild': 17.0},
        'Mercury': {'cazimi': 0.2833, 'severe': 1.5,   'moderate': 7.0,  'mild': 14.0},  # Direct
        'Jupiter': {'cazimi': 0.2833, 'severe': 3.0,   'moderate': 8.0,  'mild': 11.0},
        'Venus':   {'cazimi': 0.2833, 'severe': 2.0,   'moderate': 6.0,  'mild': 10.0},
        'Saturn':  {'cazimi': 0.2833, 'severe': 3.0,   'moderate': 10.0, 'mild': 15.0},
    }

    # 5-tier conjunction classification
    CONJUNCTION_TIERS = [
        (1.0,  'Exact',  True,  100.0),
        (3.0,  'Tight',  True,  80.0),
        (6.0,  'Close',  True,  60.0),
        (10.0, 'Wide',   False, 30.0),
        (360.0,'Ignore', False, 0.0),
    ]

    @staticmethod
    def classify_conjunction(orb: float):
        """Returns (orb_class, is_effective, base_strength)"""
        for limit, label, effective, base_strength in ConjunctionEngine.CONJUNCTION_TIERS:
            if orb < limit:
                # Interpolate strength within tier
                if label == 'Exact':
                    strength = round(90.0 + (1.0 - orb) * 10.0, 2)
                elif label == 'Tight':
                    strength = round(70.0 + ((3.0 - orb) / 2.0) * 20.0, 2)
                elif label == 'Close':
                    strength = round(40.0 + ((6.0 - orb) / 3.0) * 30.0, 2)
                elif label == 'Wide':
                    strength = round(10.0 + ((10.0 - orb) / 4.0) * 20.0, 2)
                else:
                    strength = 0.0
                strength = min(100.0, max(0.0, strength))
                return label, effective, strength
        return 'Ignore', False, 0.0

    @staticmethod
    def get_combustion_type(planet: str, orb: float, is_retrograde: bool = False) -> str:
        """Returns combustion severity string using planet-specific classical orbs."""
        orbs = ConjunctionEngine.COMBUSTION_ORBS.get(planet, None)
        if orbs is None:
            return 'None'
        # Retrograde Mercury has wider orb allowance
        mild_orb = orbs['mild']
        if planet == 'Mercury' and is_retrograde:
            mild_orb = 12.0
        if orb <= orbs['cazimi']:
            return 'Cazimi (Heart of Sun)'
        elif orb <= orbs['severe']:
            return 'Severe Combustion'
        elif orb <= orbs['moderate']:
            return 'Moderate Combustion'
        elif orb <= mild_orb:
            return 'Mild Combustion'
        return 'None'

    @staticmethod
    def calculate_conjunctions(planets_data: dict) -> dict:
        conjunctions = []
        planetary_wars = []
        stelliums = []

        planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        
        # Group planets by sign
        sign_groups = {i: [] for i in range(12)}
        for p in planet_names:
            if p in planets_data:
                s_idx = planets_data[p].get('sign_index', 0)
                sign_groups[s_idx].append(p)

        for p1_idx in range(len(planet_names)):
            p1 = planet_names[p1_idx]
            if p1 not in planets_data:
                continue
            d1 = planets_data[p1]
            lon1 = d1.get('sidereal_lon', 0.0)
            sign1 = d1.get('sign_index', 0)
            lat1 = d1.get('latitude', d1.get('declination', 0.0))  # celestial latitude

            for p2_idx in range(p1_idx + 1, len(planet_names)):
                p2 = planet_names[p2_idx]
                if p2 not in planets_data:
                    continue
                d2 = planets_data[p2]
                lon2 = d2.get('sidereal_lon', 0.0)
                sign2 = d2.get('sign_index', 0)
                lat2 = d2.get('latitude', d2.get('declination', 0.0))

                if sign1 == sign2:
                    orb = abs(lon1 - lon2)
                    orb_class, is_effective, conj_strength = ConjunctionEngine.classify_conjunction(orb)

                    # Combustion check (Sun involved)
                    combustion_type = 'None'
                    sun_in_pair = p1 == 'Sun' or p2 == 'Sun'
                    if sun_in_pair:
                        other_p = p2 if p1 == 'Sun' else p1
                        other_data = d2 if p1 == 'Sun' else d1
                        if other_p not in ('Rahu', 'Ketu', 'Sun'):
                            is_retro = other_data.get('is_retrograde', False)
                            combustion_type = ConjunctionEngine.get_combustion_type(other_p, orb, is_retro)

                    conjunctions.append({
                        # ── Backward-compatible fields ──
                        "planet_1": p1,
                        "planet_2": p2,
                        "sign": ConjunctionEngine.SIGN_NAMES[sign1],
                        "orb": round(orb, 4),
                        "is_exact": orb <= 1.0,
                        "is_close": orb <= 3.3333,
                        "combustion_severity": combustion_type,
                        # ── New v2.0 fields ──
                        "orb_class": orb_class,
                        "is_effective": is_effective,
                        "conjunction_strength": round(conj_strength, 2),
                        "note": f"{orb_class} conjunction ({orb:.2f}°)" + (" — active yoga formation" if is_effective else " — same-sign proximity only, not active yoga")
                    })

                    # Graha Yuddha: Mars, Mercury, Jupiter, Venus, Saturn within 1°
                    war_candidates = ['Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
                    if p1 in war_candidates and p2 in war_candidates and orb <= 1.0:
                        # Classical rule: winner = planet with lower celestial latitude (closer to ecliptic)
                        # The planet with more southerly latitude (lower value) is considered stronger/winner
                        winner = p1 if abs(lat1) <= abs(lat2) else p2
                        loser = p2 if winner == p1 else p1
                        planetary_wars.append({
                            "planet_1": p1,
                            "planet_2": p2,
                            "sign": ConjunctionEngine.SIGN_NAMES[sign1],
                            "orb": round(orb, 4),
                            "winner": winner,
                            "loser": loser,
                            "winner_latitude": round(lat1 if winner == p1 else lat2, 4),
                            "loser_latitude": round(lat2 if winner == p1 else lat1, 4),
                            "description": f"Graha Yuddha between {p1} and {p2}. Winner: {winner} (lower celestial latitude)."
                        })

        # Stelliums (3+ planets in same sign)
        for s_idx, p_list in sign_groups.items():
            if len(p_list) >= 3:
                stelliums.append({
                    "sign": ConjunctionEngine.SIGN_NAMES[s_idx],
                    "planets_count": len(p_list),
                    "planets": p_list,
                    "is_major_stellium": len(p_list) >= 4
                })

        return {
            "conjunctions": conjunctions,
            "planetary_wars": planetary_wars,
            "stelliums": stelliums
        }
