# -*- coding: utf-8 -*-
"""
Planet Influence Network Engine v1.0.
Builds a dependency graph showing what each planet owns, occupies, aspects,
and what life areas it influences. Enables multi-dimensional planet analysis.
"""

class PlanetInfluenceNetwork:
    PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
    NATURAL_BENEFICS = {'Jupiter', 'Venus', 'Mercury', 'Moon'}
    NATURAL_MALEFICS = {'Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun'}

    # Which houses a planet primarily signifies
    PLANET_SIGNIFICATIONS = {
        'Sun': {'Career', 'Government', 'Fame', 'Health', 'Father'},
        'Moon': {'Mind', 'Mother', 'Property', 'Emotions', 'Health'},
        'Mars': {'Career', 'Property', 'Siblings', 'Accidents', 'Litigation', 'Courage'},
        'Mercury': {'Education', 'Business', 'Communication', 'Siblings', 'Trade'},
        'Jupiter': {'Wealth', 'Children', 'Education', 'Spirituality', 'Marriage'},
        'Venus': {'Marriage', 'Wealth', 'Arts', 'Vehicles', 'Property', 'Luxury'},
        'Saturn': {'Career', 'Longevity', 'Litigation', 'Property', 'Service'},
        'Rahu': {'Foreign Travel', 'Fame', 'Technology', 'Unexpected Events'},
        'Ketu': {'Spirituality', 'Accidents', 'Longevity', 'Liberation'}
    }

    # House life area mapping
    HOUSE_LIFE_AREAS = {
        1: {'Health', 'Self', 'Personality'},
        2: {'Wealth', 'Family', 'Speech'},
        3: {'Siblings', 'Courage', 'Communication'},
        4: {'Property', 'Mother', 'Education', 'Vehicles'},
        5: {'Children', 'Education', 'Intelligence', 'Speculation'},
        6: {'Health', 'Litigation', 'Enemies', 'Service'},
        7: {'Marriage', 'Business', 'Partnerships'},
        8: {'Longevity', 'Accidents', 'Inheritance', 'Occult'},
        9: {'Fortune', 'Father', 'Spirituality', 'Education', 'Foreign Travel'},
        10: {'Career', 'Government', 'Fame', 'Authority'},
        11: {'Wealth', 'Gains', 'Friends', 'Elder Siblings'},
        12: {'Foreign Travel', 'Spirituality', 'Losses', 'Moksha'}
    }

    @staticmethod
    def build(master_obj: dict) -> list:
        network = []
        planets = master_obj.get('planets', {})
        houses = master_obj.get('houses', {})
        dignities = master_obj.get('dignity', {})
        aspects = master_obj.get('planetary_aspects', [])
        planet_state = master_obj.get('planet_state', {})
        functional = master_obj.get('functional_classification', {})
        house_analysis = master_obj.get('house_analysis', {})
        shadbala = master_obj.get('shadbala', {})

        asc_lon = houses.get('ascendant_sidereal_lon', 0.0)
        asc_idx = int(asc_lon / 30.0) % 12

        def get_house(p):
            if p not in planets: return 0
            s_idx = planets[p].get('sign_index', 0)
            return ((s_idx - asc_idx + 12) % 12) + 1

        # Build owned houses map
        owned_houses_map = {p: [] for p in PlanetInfluenceNetwork.PLANETS}
        for h in range(1, 13):
            sign_idx = (asc_idx + h - 1) % 12
            lord = PlanetInfluenceNetwork.SIGN_LORDS[sign_idx]
            if lord in owned_houses_map:
                owned_houses_map[lord].append(h)

        for planet in PlanetInfluenceNetwork.PLANETS:
            if planet not in planets:
                continue

            p_house = get_house(planet)
            owns = owned_houses_map.get(planet, [])

            # Effective aspects given by this planet
            given_aspects = [
                {'to_planet': asp['target_planet'],
                 'to_house': asp['target_house'],
                 'orb': asp['orb'],
                 'is_effective': asp.get('is_effective', True),
                 'strength': asp.get('effective_strength', asp.get('strength_percentage', 50))}
                for asp in aspects
                if asp['aspecting_planet'] == planet and asp.get('is_effective', True)
            ]

            # Aspects received by this planet
            received_aspects = [
                {'from_planet': asp['aspecting_planet'],
                 'orb': asp['orb'],
                 'is_effective': asp.get('is_effective', True)}
                for asp in aspects
                if asp['target_planet'] == planet and asp.get('is_effective', True)
            ]

            # Conjunctions (same-sign planets)
            p_sign = planets[planet].get('sign_index', 0)
            conjunct_with = [
                p2 for p2 in PlanetInfluenceNetwork.PLANETS
                if p2 != planet and p2 in planets
                and planets[p2].get('sign_index', 0) == p_sign
            ]

            # Life areas influenced
            # 1. From natural significations
            areas = set(PlanetInfluenceNetwork.PLANET_SIGNIFICATIONS.get(planet, set()))
            # 2. From owned houses
            for owned_h in owns:
                areas |= PlanetInfluenceNetwork.HOUSE_LIFE_AREAS.get(owned_h, set())
            # 3. From occupied house
            areas |= PlanetInfluenceNetwork.HOUSE_LIFE_AREAS.get(p_house, set())
            # 4. From aspected houses
            for asp in given_aspects:
                areas |= PlanetInfluenceNetwork.HOUSE_LIFE_AREAS.get(asp['to_house'], set())

            # Strength from planet_state or shadbala
            state = planet_state.get(planet, {})
            net_strength = state.get('overall_strength', 50)
            sha_virupas = shadbala.get(planet, 0)
            sha_val = sha_virupas if isinstance(sha_virupas, (int, float)) else 0

            # Benefic/malefic role
            functional_benefics = functional.get('functional_benefics', [])
            functional_malefics = functional.get('functional_malefics', [])
            if planet in functional_benefics:
                func_role = 'Functional Benefic'
            elif planet in functional_malefics:
                func_role = 'Functional Malefic'
            elif planet in PlanetInfluenceNetwork.NATURAL_BENEFICS:
                func_role = 'Natural Benefic'
            else:
                func_role = 'Natural Malefic'

            # Is yogakaraka?
            is_yogakaraka = functional.get('yogakaraka', '') == planet

            network.append({
                "planet": planet,
                "house": p_house,
                "sign": dignities.get(planet, {}).get('sign', ''),
                "dignity": dignities.get(planet, {}).get('dignity_state', 'Neutral'),
                "owns_houses": owns,
                "occupies_house": p_house,
                "aspected_by": [a['from_planet'] for a in received_aspects],
                "aspects_given": given_aspects,
                "conjunct_with": conjunct_with,
                "shadbala_virupas": round(sha_val, 1),
                "net_strength": net_strength,
                "benefic_or_malefic": 'Benefic' if planet in PlanetInfluenceNetwork.NATURAL_BENEFICS else 'Malefic',
                "functional_role": func_role,
                "is_yogakaraka": is_yogakaraka,
                "life_areas_influenced": sorted(list(areas))
            })

        return network
