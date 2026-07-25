# -*- coding: utf-8 -*-
"""
Planet State Engine v1.0.
Creates a unified state object for each planet replacing scattered flags.
Includes: physical/psychological/spiritual/material/functional/overall strength,
avastha, dig_bala, retrograde/combust/exalted status, and effective_strength_label.
"""

class PlanetStateEngine:
    PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

    DIGNITY_SCORE_MAP = {
        'Exalted': 95, 'Moolatrikona': 85, 'Swakshetra (Own Sign)': 75,
        'Great Friend (Adhi Mitra)': 65, 'Friend (Mitra)': 55,
        'Neutral (Sama)': 45, 'Enemy (Shatru)': 30,
        'Great Enemy (Adhi Shatru)': 15, 'Debilitated': 5
    }

    # Natural benefic/malefic classification
    NATURAL_BENEFICS = {'Jupiter', 'Venus', 'Mercury', 'Moon'}
    NATURAL_MALEFICS = {'Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun'}

    # Spiritual affinity (Ketu and Jupiter are most spiritual)
    SPIRITUAL_AFFINITY = {
        'Jupiter': 90, 'Ketu': 85, 'Moon': 70, 'Sun': 65,
        'Venus': 55, 'Mercury': 50, 'Saturn': 45, 'Mars': 35, 'Rahu': 25
    }

    # Material affinity (Venus and Jupiter for material)
    MATERIAL_AFFINITY = {
        'Venus': 90, 'Jupiter': 85, 'Mercury': 80, 'Moon': 70,
        'Sun': 65, 'Mars': 60, 'Saturn': 55, 'Rahu': 65, 'Ketu': 20
    }

    STRENGTH_LABELS = [
        (90, 'Exceptionally Strong'),
        (75, 'Very Strong'),
        (60, 'Strong'),
        (45, 'Moderate'),
        (30, 'Weak'),
        (0,  'Very Weak')
    ]

    @staticmethod
    def get_strength_label(score: float) -> str:
        for threshold, label in PlanetStateEngine.STRENGTH_LABELS:
            if score >= threshold:
                return label
        return 'Very Weak'

    @staticmethod
    def compute(master_obj: dict) -> dict:
        planet_state = {}
        planets = master_obj.get('planets', {})
        dignities = master_obj.get('dignity', {})
        shadbala = master_obj.get('shadbala', {})
        house_analysis = master_obj.get('house_analysis', {})
        houses = master_obj.get('houses', {})
        asc_lon = houses.get('ascendant_sidereal_lon', 0.0)
        asc_idx = int(asc_lon / 30.0) % 12

        # Planet rankings for functional strength reference
        rankings = master_obj.get('planet_ranking', [])
        rank_map = {r['name']: r['score'] for r in rankings}

        for planet in PlanetStateEngine.PLANETS:
            if planet not in planets:
                continue

            p_data = planets[planet]
            d_data = dignities.get(planet, {})
            sha_virupas = shadbala.get(planet, 0)
            sha_virupas_val = sha_virupas if isinstance(sha_virupas, (int, float)) else 0

            # Basic state flags
            dignity_state = d_data.get('dignity_state', 'Neutral (Sama)')
            is_retrograde = p_data.get('is_retrograde', False)
            is_combust = p_data.get('is_combust', False)
            is_cazimi = p_data.get('is_cazimi', False)
            is_exalted = d_data.get('is_exalted', False)
            is_debilitated = d_data.get('is_debilitated', False)
            is_moolatrikona = d_data.get('is_moolatrikona', False)
            is_own_sign = d_data.get('is_own_sign', False)

            # Dig Bala from dignity engine
            dig_bala_info = d_data.get('dig_bala', {})
            dig_bala_score = dig_bala_info.get('dig_bala_score', 50)

            # Avastha from dignity engine
            avastha = d_data.get('avastha', 'Yuva (Young Adult)')
            avastha_strength = d_data.get('avastha_strength_pct', 100)

            # Dignity numeric score
            dignity_score = PlanetStateEngine.DIGNITY_SCORE_MAP.get(dignity_state, 45)

            # Shadbala ratio (required virupas varies by planet)
            REQUIRED_VIRUPAS = {
                'Sun': 390, 'Moon': 360, 'Mars': 300, 'Mercury': 420,
                'Jupiter': 390, 'Venus': 330, 'Saturn': 300
            }
            req = REQUIRED_VIRUPAS.get(planet, 300)
            if req > 0 and sha_virupas_val > 0:
                shadbala_ratio = round(sha_virupas_val / req, 3)
            else:
                shadbala_ratio = 1.0

            # PHYSICAL STRENGTH: based on Shadbala + Dig Bala
            physical_raw = min(100, sha_virupas_val / 5.0) if sha_virupas_val > 0 else 50
            physical_dig = dig_bala_score * 0.3
            physical_strength = round(min(100, physical_raw * 0.7 + physical_dig), 1)
            if is_combust and not is_cazimi:
                physical_strength = round(physical_strength * 0.6, 1)

            # PSYCHOLOGICAL STRENGTH: Moon-related planets get bonus from Moon strength
            psy_base = dignity_score * 0.6 + avastha_strength * 0.4
            if planet == 'Moon':
                psy_base = min(100, psy_base * 1.2)
            elif planet in PlanetStateEngine.NATURAL_BENEFICS:
                psy_base = min(100, psy_base * 1.1)
            psychological_strength = round(min(100, psy_base), 1)

            # SPIRITUAL STRENGTH: based on spiritual affinity + house placement
            spiritual_affinity = PlanetStateEngine.SPIRITUAL_AFFINITY.get(planet, 50)
            s_idx = p_data.get('sign_index', 0)
            house_num = ((s_idx - asc_idx + 12) % 12) + 1
            spiritual_house_bonus = 15 if house_num in [1, 5, 9, 12] else (5 if house_num in [4, 8] else 0)
            spiritual_strength = round(min(100, spiritual_affinity * 0.8 + spiritual_house_bonus), 1)

            # MATERIAL STRENGTH: Venus/Mercury/Jupiter in material houses
            material_affinity = PlanetStateEngine.MATERIAL_AFFINITY.get(planet, 50)
            material_house_bonus = 15 if house_num in [2, 6, 10, 11] else (5 if house_num in [1, 7] else 0)
            material_strength = round(min(100, material_affinity * 0.8 + material_house_bonus + dignity_score * 0.2), 1)

            # FUNCTIONAL STRENGTH: role within this chart
            functional_score = rank_map.get(planet, 50)
            functional_strength = round(min(100, functional_score), 1)

            # OVERALL STRENGTH: weighted composite
            overall = round(
                physical_strength * 0.25 +
                psychological_strength * 0.20 +
                material_strength * 0.20 +
                functional_strength * 0.20 +
                spiritual_strength * 0.10 +
                dig_bala_score * 0.05, 1
            )

            planet_state[planet] = {
                # Basic state
                "is_retrograde": is_retrograde,
                "is_combust": is_combust,
                "is_cazimi": is_cazimi,
                "is_exalted": is_exalted,
                "is_debilitated": is_debilitated,
                "is_moolatrikona": is_moolatrikona,
                "is_own_sign": is_own_sign,
                "dignity_state": dignity_state,
                "dignity_score": dignity_score,
                "house": house_num,
                # Strength dimensions
                "physical_strength": physical_strength,
                "psychological_strength": psychological_strength,
                "spiritual_strength": spiritual_strength,
                "material_strength": material_strength,
                "functional_strength": functional_strength,
                "overall_strength": overall,
                # Supporting data
                "avastha": avastha,
                "avastha_strength_pct": avastha_strength,
                "dig_bala_score": dig_bala_score,
                "shadbala_virupas": sha_virupas_val,
                "shadbala_ratio": shadbala_ratio,
                "effective_strength_label": PlanetStateEngine.get_strength_label(overall)
            }

        return planet_state
