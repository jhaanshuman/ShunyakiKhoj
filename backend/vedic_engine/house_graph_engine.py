# -*- coding: utf-8 -*-
"""
House Graph Engine v1.0.
Builds a complete self-describing node for each house.
Each house node knows its lord, occupants, aspects, supported yogas, rule count,
and prediction contribution.
"""

class HouseGraphEngine:
    SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    NATURAL_BENEFICS = {'Jupiter', 'Venus', 'Mercury', 'Moon'}
    NATURAL_MALEFICS = {'Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun'}

    HOUSE_METADATA = {
        1: {'name': 'Lagna', 'signification': 'Self, Body, Personality, Vitality', 'type': 'Kendra/Trikona'},
        2: {'name': 'Dhana Bhava', 'signification': 'Wealth, Family, Speech, Face', 'type': 'Artha'},
        3: {'name': 'Sahaja Bhava', 'signification': 'Siblings, Courage, Communication', 'type': 'Upachaya'},
        4: {'name': 'Sukha Bhava', 'signification': 'Mother, Property, Vehicles, Education', 'type': 'Kendra/Moksha'},
        5: {'name': 'Putra Bhava', 'signification': 'Children, Intelligence, Investments', 'type': 'Trikona'},
        6: {'name': 'Shatru Bhava', 'signification': 'Enemies, Debts, Health Challenges', 'type': 'Trik/Upachaya'},
        7: {'name': 'Kalatra Bhava', 'signification': 'Spouse, Partnerships, Business', 'type': 'Kendra'},
        8: {'name': 'Mrityu Bhava', 'signification': 'Longevity, Transformation, Sudden Events', 'type': 'Trik/Moksha'},
        9: {'name': 'Dharma Bhava', 'signification': 'Fortune, Father, Higher Knowledge', 'type': 'Trikona'},
        10: {'name': 'Karma Bhava', 'signification': 'Career, Authority, Reputation', 'type': 'Kendra/Artha'},
        11: {'name': 'Labha Bhava', 'signification': 'Gains, Income, Friends', 'type': 'Upachaya'},
        12: {'name': 'Vyaya Bhava', 'signification': 'Foreign Lands, Losses, Moksha', 'type': 'Trik/Moksha'}
    }

    @staticmethod
    def build(master_obj: dict) -> list:
        house_graph = []
        house_analysis = master_obj.get('house_analysis', {})
        aspects = master_obj.get('planetary_aspects', [])
        advanced_yogas = master_obj.get('advanced_yogas', [])
        yogas = master_obj.get('yogas', [])
        rule_matches = master_obj.get('rule_matches', [])
        houses = master_obj.get('houses', {})
        planets = master_obj.get('planets', {})
        dignities = master_obj.get('dignity', {})

        asc_lon = houses.get('ascendant_sidereal_lon', 0.0)
        asc_idx = int(asc_lon / 30.0) % 12

        all_yogas = list(yogas) + list(advanced_yogas)

        # Build aspect target house map
        aspecting_by_house = {h: [] for h in range(1, 13)}
        for asp in aspects:
            th = asp.get('target_house', 1)
            if 1 <= th <= 12:
                aspecting_by_house[th].append({
                    'planet': asp['aspecting_planet'],
                    'orb': asp['orb'],
                    'is_effective': asp.get('is_effective', True),
                    'aspect_type': f"{asp.get('aspect_house', 7)}th aspect"
                })

        # Build houses aspected BY each planet
        houses_aspected_by = {h: set() for h in range(1, 13)}
        for asp in aspects:
            if asp.get('is_effective', True):
                src_sign = planets.get(asp['aspecting_planet'], {}).get('sign_index', 0)
                src_house = ((src_sign - asc_idx + 12) % 12) + 1
                houses_aspected_by[src_house].add(asp['target_house'])

        # Build yoga → house mapping
        yoga_by_house = {h: [] for h in range(1, 13)}
        for y in all_yogas:
            y_name = y.get('name', '')
            rules = y.get('rules_matched', [])
            # Simple heuristic: scan rule text for house numbers
            for h in range(1, 13):
                for rule_text in rules:
                    if f"{h}th" in str(rule_text) or f"house {h}" in str(rule_text).lower():
                        if y_name not in yoga_by_house[h]:
                            yoga_by_house[h].append(y_name)
                        break

        # Build rule → house mapping
        rule_by_house = {h: 0 for h in range(1, 13)}
        for rule in rule_matches:
            for sh in rule.get('supporting_houses', []):
                if 1 <= sh <= 12:
                    rule_by_house[sh] = rule_by_house.get(sh, 0) + 1

        # Total rule count for prediction contribution
        total_rules = len(rule_matches) if rule_matches else 1

        for h in range(1, 13):
            sign_idx = (asc_idx + h - 1) % 12
            lord = HouseGraphEngine.SIGN_LORDS[sign_idx]
            sign_name = HouseGraphEngine.SIGN_NAMES[sign_idx]

            ha = house_analysis.get(f'house_{h}', {})
            lord_sign = planets.get(lord, {}).get('sign_index', 0) if lord in planets else 0
            lord_house = ((lord_sign - asc_idx + 12) % 12) + 1 if lord in planets else 0
            lord_dignity = dignities.get(lord, {}).get('dignity_state', 'Neutral')

            occupants = ha.get('occupants', [])
            aspecting_entries = aspecting_by_house.get(h, [])
            effective_aspecting = [e['planet'] for e in aspecting_entries if e.get('is_effective', True)]
            all_aspecting = [e['planet'] for e in aspecting_entries]

            aspected_by_this_house = sorted(list(houses_aspected_by.get(h, set())))
            supported_yogas = yoga_by_house.get(h, [])
            rule_count = rule_by_house.get(h, 0)
            prediction_contribution = round(rule_count / total_rules, 3) if total_rules > 0 else 0.0

            benefic_occupants = [p for p in occupants if p in HouseGraphEngine.NATURAL_BENEFICS]
            malefic_occupants = [p for p in occupants if p in HouseGraphEngine.NATURAL_MALEFICS]
            benefic_aspecting = [p for p in effective_aspecting if p in HouseGraphEngine.NATURAL_BENEFICS]
            malefic_aspecting = [p for p in effective_aspecting if p in HouseGraphEngine.NATURAL_MALEFICS]

            strength_score = ha.get('house_score', 50.0)
            house_meta = HouseGraphEngine.HOUSE_METADATA.get(h, {})

            house_graph.append({
                "house": h,
                "house_name": house_meta.get('name', f'House {h}'),
                "signification": house_meta.get('signification', ''),
                "house_type": house_meta.get('type', 'Neutral'),
                "sign": sign_name,
                "sign_index": sign_idx,
                "lord": lord,
                "lord_house": lord_house,
                "lord_dignity": lord_dignity,
                "occupants": occupants,
                "benefic_occupants": benefic_occupants,
                "malefic_occupants": malefic_occupants,
                "aspecting_planets": all_aspecting,
                "effective_aspecting_planets": effective_aspecting,
                "benefic_aspecting": benefic_aspecting,
                "malefic_aspecting": malefic_aspecting,
                "aspected_houses_from_here": aspected_by_this_house,
                "supported_yogas": supported_yogas,
                "rule_count": rule_count,
                "prediction_contribution": prediction_contribution,
                "strength_score": strength_score,
                "is_afflicted": ha.get('is_afflicted', False),
                "is_protected": ha.get('is_protected', False),
                "net_influence_score": ha.get('net_influence_score', 0),
                "strength_rating": ha.get('strength_rating', 'Moderate')
            })

        return house_graph
