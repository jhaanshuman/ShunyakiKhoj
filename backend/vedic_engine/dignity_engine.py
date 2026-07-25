# -*- coding: utf-8 -*-
"""
Complete Dignity & Friendship Engine (Panchadha Sambandha) v2.0.
Determines exact planetary dignity across 9 states based on BPHS rules.
New: Dig Bala (Directional Strength), Avastha (planetary age states),
dignity_score (numeric 0-100), corrected sign field.
"""

class DignityEngine:
    PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    EXALTATION_DEGREES = {
        'Sun': (0, 10.0), 'Moon': (1, 3.0), 'Mars': (9, 28.0),
        'Mercury': (5, 15.0), 'Jupiter': (3, 5.0), 'Venus': (11, 27.0),
        'Saturn': (6, 20.0), 'Rahu': (1, 15.0), 'Ketu': (7, 15.0)
    }
    
    DEBILITATION_DEGREES = {
        'Sun': (6, 10.0), 'Moon': (7, 3.0), 'Mars': (3, 28.0),
        'Mercury': (11, 15.0), 'Jupiter': (9, 5.0), 'Venus': (5, 27.0),
        'Saturn': (0, 20.0), 'Rahu': (7, 15.0), 'Ketu': (1, 15.0)
    }

    MOOLATRIKONA = {
        'Sun': (4, 0.0, 20.0), 'Moon': (1, 3.0, 30.0), 'Mars': (0, 0.0, 12.0),
        'Mercury': (5, 15.0, 20.0), 'Jupiter': (8, 0.0, 10.0),
        'Venus': (6, 0.0, 15.0), 'Saturn': (10, 0.0, 20.0)
    }

    OWN_SIGNS = {
        'Sun': [4], 'Moon': [3], 'Mars': [0, 7], 'Mercury': [2, 5],
        'Jupiter': [8, 11], 'Venus': [1, 6], 'Saturn': [9, 10],
        'Rahu': [10], 'Ketu': [7]
    }

    PERMANENT_FRIENDS = {
        'Sun': {'Moon': 'F', 'Mars': 'F', 'Jupiter': 'F', 'Venus': 'E', 'Saturn': 'E', 'Mercury': 'N', 'Rahu': 'E', 'Ketu': 'E'},
        'Moon': {'Sun': 'F', 'Mercury': 'F', 'Mars': 'N', 'Jupiter': 'N', 'Venus': 'N', 'Saturn': 'N', 'Rahu': 'E', 'Ketu': 'E'},
        'Mars': {'Sun': 'F', 'Moon': 'F', 'Jupiter': 'F', 'Mercury': 'E', 'Venus': 'N', 'Saturn': 'N', 'Rahu': 'E', 'Ketu': 'N'},
        'Mercury': {'Sun': 'F', 'Venus': 'F', 'Moon': 'E', 'Mars': 'N', 'Jupiter': 'N', 'Saturn': 'N', 'Rahu': 'F', 'Ketu': 'N'},
        'Jupiter': {'Sun': 'F', 'Moon': 'F', 'Mars': 'F', 'Mercury': 'E', 'Venus': 'E', 'Saturn': 'N', 'Rahu': 'N', 'Ketu': 'F'},
        'Venus': {'Mercury': 'F', 'Saturn': 'F', 'Sun': 'E', 'Moon': 'E', 'Mars': 'N', 'Jupiter': 'N', 'Rahu': 'F', 'Ketu': 'F'},
        'Saturn': {'Mercury': 'F', 'Venus': 'F', 'Sun': 'E', 'Moon': 'E', 'Mars': 'E', 'Jupiter': 'N', 'Rahu': 'F', 'Ketu': 'E'},
        'Rahu': {'Mercury': 'F', 'Venus': 'F', 'Saturn': 'F', 'Sun': 'E', 'Moon': 'E', 'Mars': 'E', 'Jupiter': 'N', 'Ketu': 'E'},
        'Ketu': {'Sun': 'E', 'Moon': 'E', 'Mars': 'N', 'Mercury': 'N', 'Jupiter': 'F', 'Venus': 'F', 'Saturn': 'E', 'Rahu': 'E'}
    }

    SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']

    # Dig Bala: planet -> house where it has max directional strength
    DIG_BALA_HOUSE = {
        'Sun': 10, 'Mars': 10,
        'Moon': 4, 'Venus': 4,
        'Mercury': 1, 'Jupiter': 1,
        'Saturn': 7,
        'Rahu': 4, 'Ketu': 4
    }

    # Dignity numeric scores
    DIGNITY_SCORES = {
        'Exalted': 95, 'Moolatrikona': 85, 'Swakshetra (Own Sign)': 75,
        'Great Friend (Adhi Mitra)': 65, 'Friend (Mitra)': 55, 'Neutral (Sama)': 45,
        'Enemy (Shatru)': 30, 'Great Enemy (Adhi Shatru)': 15, 'Debilitated': 5
    }

    @staticmethod
    def get_dig_bala_score(planet: str, house_num: int) -> dict:
        """Calculate Directional Strength (Dig Bala) score 0-100."""
        best_house = DignityEngine.DIG_BALA_HOUSE.get(planet, 1)
        worst_house = ((best_house - 1 + 6) % 12) + 1  # Opposite house
        
        if house_num == best_house:
            score = 100
            direction = "Full Dig Bala"
        elif house_num == worst_house:
            score = 0
            direction = "No Dig Bala (opposite)"
        else:
            # Distance from best house (0-6, then mirror)
            dist = abs(house_num - best_house)
            if dist > 6:
                dist = 12 - dist
            score = max(0, round(100 - (dist / 6.0) * 100, 0))
            direction = f"Partial Dig Bala"
        
        return {
            "best_direction_house": best_house,
            "current_house": house_num,
            "dig_bala_score": int(score),
            "dig_bala_label": direction
        }

    @staticmethod
    def get_avastha(deg: float) -> dict:
        """Determine Avastha (planetary age state) from degrees within sign."""
        if deg < 6.0:
            return {"avastha": "Bala (Infant)", "avastha_strength_pct": 50, "avastha_contribution": -25}
        elif deg < 12.0:
            return {"avastha": "Kumara (Youth)", "avastha_strength_pct": 75, "avastha_contribution": -10}
        elif deg < 18.0:
            return {"avastha": "Yuva (Young Adult)", "avastha_strength_pct": 100, "avastha_contribution": 0}
        elif deg < 24.0:
            return {"avastha": "Vriddha (Mature)", "avastha_strength_pct": 75, "avastha_contribution": -10}
        else:
            return {"avastha": "Mrita (Dead)", "avastha_strength_pct": 25, "avastha_contribution": -40}

    @staticmethod
    def calculate_complete_dignities(planets_data: dict, ascendant_sign_idx: int = None) -> dict:
        dignities = {}

        # Compute Tatkalika (Temporary) Relationships
        tatkalika = {}
        for p1 in DignityEngine.PLANETS:
            tatkalika[p1] = {}
            if p1 not in planets_data:
                continue
            s1 = planets_data[p1].get('sign_index', 0)
            for p2 in DignityEngine.PLANETS:
                if p1 == p2 or p2 not in planets_data:
                    continue
                s2 = planets_data[p2].get('sign_index', 0)
                diff = (s2 - s1 + 12) % 12
                is_temp_friend = diff in [1, 2, 3, 9, 10, 11]
                tatkalika[p1][p2] = 'F' if is_temp_friend else 'E'

        for p in DignityEngine.PLANETS:
            if p not in planets_data:
                continue
            d_info = planets_data[p]
            s_idx = d_info.get('sign_index', 0)
            deg = d_info.get('sign_degree', 0.0)

            ex_sign, ex_deg = DignityEngine.EXALTATION_DEGREES.get(p, (-1, -1))
            deb_sign, deb_deg = DignityEngine.DEBILITATION_DEGREES.get(p, (-1, -1))
            
            dignity_state = "Neutral (Sama)"
            
            if s_idx == ex_sign:
                dignity_state = "Exalted"
            elif s_idx == deb_sign:
                dignity_state = "Debilitated"
            elif p in DignityEngine.MOOLATRIKONA:
                mt_sign, mt_start, mt_end = DignityEngine.MOOLATRIKONA[p]
                if s_idx == mt_sign and mt_start <= deg <= mt_end:
                    dignity_state = "Moolatrikona"
            
            if dignity_state == "Neutral (Sama)":
                if s_idx in DignityEngine.OWN_SIGNS.get(p, []):
                    dignity_state = "Swakshetra (Own Sign)"
                else:
                    sign_lord = DignityEngine.SIGN_LORDS[s_idx]
                    if sign_lord == p:
                        dignity_state = "Swakshetra (Own Sign)"
                    else:
                        perm = DignityEngine.PERMANENT_FRIENDS.get(p, {}).get(sign_lord, 'N')
                        temp = tatkalika.get(p, {}).get(sign_lord, 'E')

                        score = (1 if perm == 'F' else (-1 if perm == 'E' else 0)) + \
                                (1 if temp == 'F' else -1)
                        
                        if score == 2:
                            dignity_state = "Great Friend (Adhi Mitra)"
                        elif score == 1:
                            dignity_state = "Friend (Mitra)"
                        elif score == 0:
                            dignity_state = "Neutral (Sama)"
                        elif score == -1:
                            dignity_state = "Enemy (Shatru)"
                        elif score == -2:
                            dignity_state = "Great Enemy (Adhi Shatru)"

            # Sign lord for relationship info
            sign_lord = DignityEngine.SIGN_LORDS[s_idx]
            perm_rel_label = {'F': 'Friend', 'E': 'Enemy', 'N': 'Neutral'}.get(
                DignityEngine.PERMANENT_FRIENDS.get(p, {}).get(sign_lord, 'N'), 'Neutral')
            temp_rel_label = {'F': 'Friend', 'E': 'Enemy'}.get(
                tatkalika.get(p, {}).get(sign_lord, 'E'), 'Enemy')

            # Dig Bala
            house_num = 1
            if ascendant_sign_idx is not None:
                house_num = ((s_idx - ascendant_sign_idx + 12) % 12) + 1
            dig_bala = DignityEngine.get_dig_bala_score(p, house_num)

            # Avastha
            avastha = DignityEngine.get_avastha(deg)

            # Dignity score
            dignity_score = DignityEngine.DIGNITY_SCORES.get(dignity_state, 45)

            dignities[p] = {
                # ── Backward-compatible fields ──
                "sign": DignityEngine.SIGN_NAMES[s_idx],   # FIX: was SIGN_LORDS, now SIGN_NAMES
                "sign_index": s_idx,
                "sign_lord": sign_lord,                      # Correctly shows lord name
                "dignity_state": dignity_state,
                "is_exalted": dignity_state == "Exalted",
                "is_debilitated": dignity_state == "Debilitated",
                "is_moolatrikona": dignity_state == "Moolatrikona",
                "is_own_sign": "Swakshetra" in dignity_state,
                "panchadha_relationships": tatkalika.get(p, {}),
                # ── New v2.0 fields ──
                "dignity_score": dignity_score,
                "permanent_relationship_with_lord": perm_rel_label,
                "temporary_relationship_with_lord": temp_rel_label,
                "compound_relationship": dignity_state if dignity_state not in ['Exalted', 'Debilitated', 'Moolatrikona', 'Swakshetra (Own Sign)'] else 'N/A',
                "dig_bala": dig_bala,
                **avastha
            }

        return dignities
