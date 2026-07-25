# -*- coding: utf-8 -*-
"""
Deterministic Prediction Rule Engine v3.0.
Evaluates 17 core life domains with 75+ multi-condition rules.
Each rule carries: evidence_chain, conflicting_factors, astrological_logic, dynamic confidence.
Domains: Career, Marriage, Wealth, Education, Children, Property, Siblings, Parents,
Foreign Travel, Spirituality, Litigation, Business, Government, Fame, Longevity,
Accidents, Health.
"""

class RuleEngine:

    NATURAL_BENEFICS = {'Jupiter', 'Venus', 'Mercury', 'Moon'}
    NATURAL_MALEFICS = {'Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun'}
    KENDRA_HOUSES = {1, 4, 7, 10}
    TRIKONA_HOUSES = {1, 5, 9}
    TRIK_HOUSES = {6, 8, 12}

    @staticmethod
    def _get_h(houses_analysis: dict, num: int) -> dict:
        return houses_analysis.get(f'house_{num}', {})

    @staticmethod
    def _house_score(houses_analysis: dict, num: int) -> float:
        return RuleEngine._get_h(houses_analysis, num).get('house_score', 50.0)

    @staticmethod
    def _lord(houses_analysis: dict, num: int) -> str:
        return RuleEngine._get_h(houses_analysis, num).get('house_lord', '')

    @staticmethod
    def _lord_house(houses_analysis: dict, num: int) -> int:
        return RuleEngine._get_h(houses_analysis, num).get('lord_location_house', 1)

    @staticmethod
    def _lord_dignity(houses_analysis: dict, num: int) -> str:
        return RuleEngine._get_h(houses_analysis, num).get('lord_dignity', 'Neutral')

    @staticmethod
    def _is_exalted(dignity: str) -> bool:
        return 'Exalted' in dignity

    @staticmethod
    def _is_own(dignity: str) -> bool:
        return 'Swakshetra' in dignity or 'Moolatrikona' in dignity

    @staticmethod
    def _is_debilitated(dignity: str) -> bool:
        return 'Debilitated' in dignity

    @staticmethod
    def _is_enemy(dignity: str) -> bool:
        return 'Enemy' in dignity

    @staticmethod
    def _in_kendra(house: int) -> bool:
        return house in RuleEngine.KENDRA_HOUSES

    @staticmethod
    def _in_trikona(house: int) -> bool:
        return house in RuleEngine.TRIKONA_HOUSES

    @staticmethod
    def _in_trik(house: int) -> bool:
        return house in RuleEngine.TRIK_HOUSES

    @staticmethod
    def _shadbala_strong(shadbala: dict, planet: str, threshold: float = 350.0) -> bool:
        return shadbala.get(planet, 0) >= threshold

    @staticmethod
    def _yoga_present(yoga_names: list, keywords: list) -> bool:
        for y in yoga_names:
            for kw in keywords:
                if kw.lower() in y.lower():
                    return True
        return False

    @staticmethod
    def _adjust_confidence(base: float, conflicting: list) -> float:
        """Reduce confidence by 3-8% per conflicting factor."""
        reduction = min(len(conflicting) * 5.0, 25.0)
        return max(40.0, round(base - reduction, 1))

    @staticmethod
    def _make_rule(rule_id, title, domain, base_confidence, strength,
                   conditions, evidence_chain, conflicting_factors,
                   supporting_planets, supporting_houses, supporting_yogas,
                   astrological_logic, description):
        confidence = RuleEngine._adjust_confidence(base_confidence, conflicting_factors)
        return {
            "id": rule_id,
            "title": title,
            "domain": domain,
            "confidence": confidence,
            "base_confidence": base_confidence,
            "strength": round(strength, 2),
            "matched_conditions": conditions,
            "evidence_chain": evidence_chain,
            "conflicting_factors": conflicting_factors,
            "supporting_planets": supporting_planets,
            "supporting_houses": supporting_houses,
            "supporting_yogas": supporting_yogas,
            "astrological_logic": astrological_logic,
            "description": description
        }

    @staticmethod
    def evaluate_rules(master_obj: dict) -> list:
        rule_matches = []
        
        ha = master_obj.get('house_analysis', {})
        functional = master_obj.get('functional_classification', {})
        yogas_list = master_obj.get('yogas', [])
        advanced_yogas = master_obj.get('advanced_yogas', [])
        rankings = master_obj.get('planet_ranking', [])
        dignities = master_obj.get('dignity', {})
        shadbala = master_obj.get('shadbala', {})
        planets = master_obj.get('planets', {})
        aspects = master_obj.get('planetary_aspects', [])
        
        # Helpers
        H = RuleEngine._house_score
        L = RuleEngine._lord
        LH = RuleEngine._lord_house
        LD = RuleEngine._lord_dignity

        all_yogas_raw = list(yogas_list) + list(advanced_yogas)
        yoga_names = [y.get('name', '') for y in all_yogas_raw]
        
        top_planet = rankings[0]['name'] if rankings else 'Jupiter'
        
        def get_sign_idx(p):
            return planets.get(p, {}).get('sign_index', -1)
        
        def get_house_of(p):
            """Return house number for a planet (1-12)."""
            if p not in planets:
                return 0
            asc_lon = master_obj.get('houses', {}).get('ascendant_sidereal_lon', 0.0)
            asc_idx = int(asc_lon / 30.0) % 12
            s_idx = planets[p].get('sign_index', 0)
            return ((s_idx - asc_idx + 12) % 12) + 1

        def planet_in_house(p, h_num):
            return get_house_of(p) == h_num

        def planet_aspects_house(p, h_num):
            """Check if planet effectively aspects a house."""
            for asp in aspects:
                if asp.get('aspecting_planet') == p and asp.get('target_house') == h_num:
                    if asp.get('is_effective', asp.get('is_valid', True)):
                        return True
            return False

        def get_occupants(h_num):
            return ha.get(f'house_{h_num}', {}).get('occupants', [])

        def benefic_in_house(h_num):
            return any(p in RuleEngine.NATURAL_BENEFICS for p in get_occupants(h_num))

        def malefic_in_house(h_num):
            return any(p in RuleEngine.NATURAL_MALEFICS for p in get_occupants(h_num))

        def jup_aspects(h_num):
            return planet_aspects_house('Jupiter', h_num)

        def saturn_aspects(h_num):
            return planet_aspects_house('Saturn', h_num)

        def rahu_in_house(h_num):
            return planet_in_house('Rahu', h_num)

        def ketu_in_house(h_num):
            return planet_in_house('Ketu', h_num)

        # =====================================================================
        # DOMAIN 1: CAREER (8 rules)
        # =====================================================================
        h10s = H(ha, 10)
        h10_lord = L(ha, 10)
        h10_lord_house = LH(ha, 10)
        h10_lord_dignity = LD(ha, 10)
        h6s = H(ha, 6)
        h1s = H(ha, 1)

        # RULE_CAR_001: Strong 10th House
        if h10s >= 70.0:
            evidence = [f"10th house score = {h10s}/100"]
            conflicts = []
            if malefic_in_house(10): conflicts.append("Malefic occupying 10th house")
            if RuleEngine._in_trik(h10_lord_house): conflicts.append(f"10th lord in trik house ({h10_lord_house})")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_001", "Strong 10th House — Executive Authority", "Career",
                92.0, h10s, [f"10th house score ≥ 70 ({h10s}/100)"],
                evidence, conflicts,
                [h10_lord, top_planet], [10, h10_lord_house],
                [y for y in yoga_names if any(kw in y for kw in ['Raja', 'Mahapurusha', 'Budhaditya'])],
                "Strong 10th house → Career lord well-placed → Executive authority",
                "High career authority, rapid growth, and public recognition."
            ))

        # RULE_CAR_002: 10th Lord Exalted
        if RuleEngine._is_exalted(h10_lord_dignity):
            evidence = [f"10th lord {h10_lord} is Exalted", f"Placed in house {h10_lord_house}"]
            conflicts = []
            if RuleEngine._in_trik(h10_lord_house): conflicts.append(f"{h10_lord} in trik house despite exaltation")
            if not RuleEngine._shadbala_strong(shadbala, h10_lord, 300): conflicts.append(f"{h10_lord} Shadbala below 300 Virupas")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_002", "Exalted 10th Lord — Career Peak", "Career",
                95.0, 90.0, [f"10th lord {h10_lord} is Exalted"],
                evidence, conflicts,
                [h10_lord], [10, h10_lord_house],
                [y for y in yoga_names if 'Raja' in y or 'Mahapurusha' in y],
                f"10th lord {h10_lord} → Exalted dignity → Maximum career potential",
                "Career at its zenith — achievement of highest professional status."
            ))

        # RULE_CAR_003: 10th Lord in Kendra/Trikona
        if RuleEngine._in_kendra(h10_lord_house) or RuleEngine._in_trikona(h10_lord_house):
            evidence = [f"10th lord {h10_lord} in house {h10_lord_house} (Kendra/Trikona)", f"House score: {h10s}/100"]
            conflicts = []
            if RuleEngine._is_debilitated(h10_lord_dignity) or RuleEngine._is_enemy(h10_lord_dignity):
                conflicts.append(f"{h10_lord} in unfriendly dignity")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_003", "10th Lord in Angular/Trine — Stable Career", "Career",
                88.0, h10s, [f"10th lord in Kendra/Trikona house {h10_lord_house}"],
                evidence, conflicts,
                [h10_lord], [10, h10_lord_house],
                [y for y in yoga_names if 'Raja' in y],
                f"10th lord {h10_lord} in Kendra/Trikona → Career lord empowered → Professional stability",
                "Stable career trajectory with consistent growth and achievement."
            ))

        # RULE_CAR_004: Jupiter Aspects 10th House
        if jup_aspects(10):
            jup_dignity = dignities.get('Jupiter', {}).get('dignity_state', '')
            evidence = ["Jupiter effectively aspects 10th house", f"Jupiter dignity: {jup_dignity}"]
            conflicts = []
            if rahu_in_house(10): conflicts.append("Rahu in 10th may cause unexpected career changes")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_004", "Jupiter Aspects 10th — Wisdom & Ethical Career", "Career",
                90.0, 82.0, ["Jupiter effectively aspects 10th house"],
                evidence, conflicts,
                ['Jupiter'], [10],
                [y for y in yoga_names if 'Hamsa' in y or 'Gajakesari' in y],
                "Jupiter (Dharma karaka) aspects 10th → Ethical and wisdom-based career elevation",
                "Career in advisory, legal, teaching, or consulting roles with high ethical standing."
            ))

        # RULE_CAR_005: Sun Strong in 10th (Digbala)
        if planet_in_house('Sun', 10) and H(ha, 10) >= 55:
            sun_dig = dignities.get('Sun', {}).get('dignity_state', '')
            evidence = ["Sun in 10th house (Digbala position)", f"Sun dignity: {sun_dig}"]
            conflicts = []
            if RuleEngine._is_debilitated(sun_dig): conflicts.append("Sun debilitated reduces government authority")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_005", "Sun in 10th — Government & Leadership Authority", "Career",
                88.0, 85.0, ["Sun placed in 10th house"],
                evidence, conflicts,
                ['Sun'], [10],
                [y for y in yoga_names if 'Raja' in y or 'Budhaditya' in y],
                "Sun (Atmakaraka) in Digbala position (10th) → Natural leadership and government authority",
                "Authority in government, administration, or leadership positions."
            ))

        # RULE_CAR_006: 10th Lord Conjunct Benefic
        benefic_conjunction_10lord = any(
            p in RuleEngine.NATURAL_BENEFICS and p != h10_lord and get_house_of(p) == h10_lord_house
            for p in ['Jupiter', 'Venus', 'Mercury', 'Moon']
        )
        if benefic_conjunction_10lord and h10s >= 55:
            evidence = [f"10th lord {h10_lord} conjunct with natural benefic in house {h10_lord_house}"]
            conflicts = []
            if malefic_in_house(h10_lord_house): conflicts.append("Malefic also conjunct with 10th lord")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_006", "10th Lord Conjunct Benefic — Career Elevation", "Career",
                86.0, 78.0, [f"10th lord {h10_lord} conjunct natural benefic"],
                evidence, conflicts,
                [h10_lord], [10, h10_lord_house],
                [y for y in yoga_names if 'Raja' in y or 'Dhana' in y],
                f"10th lord {h10_lord} with benefic planet → Career magnified by wisdom/grace",
                "Career gains through beneficial partnerships, mentors, or professional alliances."
            ))

        # RULE_CAR_007: Shadbala Strong 10th Lord
        if RuleEngine._shadbala_strong(shadbala, h10_lord, 400) and h10s >= 60:
            sha_val = shadbala.get(h10_lord, 0)
            evidence = [f"10th lord {h10_lord} Shadbala = {sha_val} Virupas (Strong)", f"10th house score: {h10s}"]
            conflicts = []
            if RuleEngine._in_trik(h10_lord_house): conflicts.append(f"10th lord in trik despite strength")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_007", "Strong 10th Lord Shadbala — Sustained Career", "Career",
                87.0, min(100, sha_val / 6.0), [f"10th lord {h10_lord} Shadbala ≥ 400 Virupas"],
                evidence, conflicts,
                [h10_lord], [10],
                [y for y in yoga_names if 'Raja' in y or 'Mahapurusha' in y],
                f"10th lord {h10_lord} with high Shadbala ({sha_val}) → Sustained career energy over time",
                "Consistent career performance, longevity in profession, and long-term recognition."
            ))

        # RULE_CAR_008: Yoga Karaka Planet Influencing 10th
        yogakaraka = functional.get('yogakaraka', None)
        if yogakaraka and (planet_in_house(yogakaraka, 10) or planet_aspects_house(yogakaraka, 10)):
            yk_dig = dignities.get(yogakaraka, {}).get('dignity_state', 'Neutral')
            evidence = [f"Yogakaraka {yogakaraka} placed in or aspects 10th house", f"Dignity: {yk_dig}"]
            conflicts = []
            if RuleEngine._is_debilitated(yk_dig): conflicts.append(f"Yogakaraka {yogakaraka} is debilitated")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CAR_008", "Yogakaraka Planet in 10th — Peak Career Success", "Career",
                96.0, 92.0, [f"Yogakaraka {yogakaraka} influences 10th house"],
                evidence, conflicts,
                [yogakaraka], [10],
                [y for y in yoga_names if yogakaraka in y or 'Raja' in y],
                f"Yogakaraka {yogakaraka} (most benefic for lagna) → Influences career house → Peak success potential",
                "Exceptional career achievement driven by the most powerful benefic for this ascendant."
            ))

        # =====================================================================
        # DOMAIN 2: MARRIAGE (8 rules)
        # =====================================================================
        h7s = H(ha, 7)
        h7_lord = L(ha, 7)
        h7_lord_house = LH(ha, 7)
        h7_lord_dignity = LD(ha, 7)
        h5s = H(ha, 5)
        h2s = H(ha, 2)
        venus_house = get_house_of('Venus')
        venus_dig = dignities.get('Venus', {}).get('dignity_state', 'Neutral')

        # RULE_MAR_001: Strong 7th House
        if h7s >= 65.0:
            evidence = [f"7th house score = {h7s}/100", f"7th lord: {h7_lord}"]
            conflicts = []
            if malefic_in_house(7): conflicts.append("Malefic in 7th house can cause marital tensions")
            if RuleEngine._in_trik(h7_lord_house): conflicts.append(f"7th lord in trik house {h7_lord_house}")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_001", "Harmonious 7th House — Marital Fortune", "Marriage",
                92.0, h7s, [f"7th house score ≥ 65 ({h7s}/100)"],
                evidence, conflicts,
                [h7_lord, 'Venus'], [7, h7_lord_house],
                [y for y in yoga_names if any(kw in y for kw in ['Malavya', 'Lakshmi', 'Gajakesari'])],
                "Strong 7th house → Benefic lord placement → Harmonious marital partnership",
                "Supportive marital partner, auspicious family harmony, and fruitful alliances."
            ))

        # RULE_MAR_002: Venus Exalted or Own Sign
        if RuleEngine._is_exalted(venus_dig) or RuleEngine._is_own(venus_dig):
            evidence = [f"Venus in {venus_dig}", f"Venus in house {venus_house}"]
            conflicts = []
            if planet_in_house('Rahu', venus_house): conflicts.append("Rahu conjunct Venus — unconventional relationships")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_002", "Strong Venus — Beauty, Love & Partnership", "Marriage",
                93.0, 88.0, [f"Venus in {venus_dig}"],
                evidence, conflicts,
                ['Venus'], [7, venus_house],
                [y for y in yoga_names if 'Malavya' in y or 'Lakshmi' in y],
                "Venus (Kalatra karaka) in own/exalted sign → Strongest signifier of marriage prosperity",
                "Beautiful, loyal partner; artistic home environment; marital bliss."
            ))

        # RULE_MAR_003: 7th Lord in Kendra/Trikona
        if RuleEngine._in_kendra(h7_lord_house) or RuleEngine._in_trikona(h7_lord_house):
            evidence = [f"7th lord {h7_lord} in house {h7_lord_house} (Kendra/Trikona)"]
            conflicts = []
            if RuleEngine._is_debilitated(h7_lord_dignity): conflicts.append(f"7th lord {h7_lord} debilitated")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_003", "7th Lord in Angular/Trine — Stable Marriage", "Marriage",
                88.0, h7s, [f"7th lord {h7_lord} in Kendra/Trikona house {h7_lord_house}"],
                evidence, conflicts,
                [h7_lord], [7, h7_lord_house],
                [],
                f"7th lord {h7_lord} in auspicious house → Marriage partner well-supported",
                "Stable, long-lasting marriage with loyal and supportive partner."
            ))

        # RULE_MAR_004: Jupiter Aspects 7th
        if jup_aspects(7):
            evidence = ["Jupiter effectively aspects 7th house", f"7th house score: {h7s}"]
            conflicts = []
            if rahu_in_house(7): conflicts.append("Rahu in 7th may cause delays or unconventional marriage")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_004", "Jupiter Aspects 7th — Dharmic Marriage", "Marriage",
                91.0, 85.0, ["Jupiter aspects 7th house"],
                evidence, conflicts,
                ['Jupiter'], [7],
                [y for y in yoga_names if 'Hamsa' in y or 'Gajakesari' in y],
                "Jupiter (Dharma karaka) aspects 7th → Marriage blessed by righteousness and wisdom",
                "Virtuous and educated partner; dharmic household; long and happy marriage."
            ))

        # RULE_MAR_005: 5th Lord Connects to 7th (Love-Marriage Yoga)
        h5_lord = L(ha, 5)
        h5_lord_house = LH(ha, 5)
        if h5_lord_house == 7 or h7_lord_house == 5:
            evidence = [f"5th lord {h5_lord} in 7th OR 7th lord {h7_lord} in 5th — romance-marriage link"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_005", "5th-7th Lord Exchange — Love Marriage Yoga", "Marriage",
                87.0, 80.0, ["5th and 7th lords in mutual exchange or connection"],
                evidence, conflicts,
                [h5_lord, h7_lord], [5, 7],
                [y for y in yoga_names if 'Malavya' in y],
                "5th (love/romance) connects with 7th (marriage) → Love-based marriage",
                "Marriage founded on deep romantic connection and emotional bond."
            ))

        # RULE_MAR_006: 7th Lord Exalted
        if RuleEngine._is_exalted(h7_lord_dignity):
            evidence = [f"7th lord {h7_lord} Exalted in house {h7_lord_house}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_006", "Exalted 7th Lord — Elevated Marital Status", "Marriage",
                95.0, 92.0, [f"7th lord {h7_lord} is Exalted"],
                evidence, conflicts,
                [h7_lord], [7, h7_lord_house],
                [y for y in yoga_names if 'Raja' in y or 'Malavya' in y],
                f"7th lord {h7_lord} in peak dignity → Marriage to highly accomplished and noble partner",
                "Marriage to a distinguished, accomplished, and virtuous partner."
            ))

        # RULE_MAR_007: Malefic in 7th (Delay/Challenge)
        if malefic_in_house(7) and h7s < 55:
            mal_7 = [p for p in get_occupants(7) if p in RuleEngine.NATURAL_MALEFICS]
            evidence = [f"Malefic(s) {mal_7} in 7th house", f"7th house score: {h7s}"]
            conflicts = []
            if jup_aspects(7): conflicts.append("Jupiter's aspect on 7th mitigates malefic influence")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_007", "Malefic in 7th — Marital Challenges", "Marriage",
                82.0, 100 - h7s, [f"Malefic {mal_7} in 7th, 7th house score < 55"],
                evidence, conflicts,
                mal_7, [7],
                [],
                f"Malefic {mal_7} in partnership house → Friction and delay in marriage",
                "Marriage may face delays, conflicts, or require significant compromise."
            ))

        # RULE_MAR_008: 2nd House (Family) Strong — Happy Family Life
        if h2s >= 65.0 and h7s >= 55.0:
            evidence = [f"2nd house (family) score = {h2s}", f"7th house score = {h7s}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_MAR_008", "Strong 2nd House — Blissful Family Environment", "Marriage",
                85.0, (h2s + h7s) / 2, ["2nd house ≥ 65 and 7th house ≥ 55"],
                evidence, conflicts,
                [L(ha, 2), h7_lord], [2, 7],
                [y for y in yoga_names if 'Lakshmi' in y or 'Gajakesari' in y],
                "2nd house (Kutumba) strong → Family happiness + 7th house strength → Marital bliss",
                "Warm family environment, pleasant domestic life, and family support after marriage."
            ))

        # =====================================================================
        # DOMAIN 3: WEALTH & FINANCE (6 rules)
        # =====================================================================
        h11s = H(ha, 11)
        h9s = H(ha, 9)
        h2_lord = L(ha, 2)
        h11_lord = L(ha, 11)

        # RULE_WLT_001: Combined 2nd+11th Strong
        wealth_score = round((h2s + h11s) / 2.0, 2)
        if wealth_score >= 65.0:
            evidence = [f"2nd house score = {h2s}", f"11th house score = {h11s}", f"Average = {wealth_score}"]
            conflicts = []
            if RuleEngine._in_trik(LH(ha, 2)) and RuleEngine._in_trik(LH(ha, 11)):
                conflicts.append("Both wealth lords in trik houses")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_WLT_001", "Prosperous Wealth Houses — Financial Holdings", "Wealth",
                93.0, wealth_score, [f"Combined 2nd+11th average ≥ 65 ({wealth_score})"],
                evidence, conflicts,
                [h2_lord, h11_lord], [2, 11, 9],
                [y for y in yoga_names if any(kw in y for kw in ['Dhana', 'Chandra Mangala', 'Gajakesari'])],
                "2nd house (accumulated wealth) + 11th house (income gains) both strong → Financial prosperity",
                "Steady wealth accumulation, profitable income, and strong monetary foundation."
            ))

        # RULE_WLT_002: Jupiter Strong in 2nd or 11th or 9th
        jup_h = get_house_of('Jupiter')
        jup_dig = dignities.get('Jupiter', {}).get('dignity_state', 'Neutral')
        if jup_h in [2, 5, 9, 11] and RuleEngine._shadbala_strong(shadbala, 'Jupiter', 320):
            evidence = [f"Jupiter in house {jup_h}", f"Jupiter dignity: {jup_dig}", f"Shadbala: {shadbala.get('Jupiter', 0)} Virupas"]
            conflicts = []
            if ketu_in_house(jup_h): conflicts.append("Ketu conjunct Jupiter reduces wealth signification")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_WLT_002", "Strong Jupiter in Wealth/Trikona — Dhana Yoga", "Wealth",
                91.0, 85.0, [f"Jupiter in house {jup_h} with strong Shadbala"],
                evidence, conflicts,
                ['Jupiter'], [jup_h],
                [y for y in yoga_names if 'Gajakesari' in y or 'Hamsa' in y or 'Dhana' in y],
                f"Jupiter (Dhana karaka) in wealth house {jup_h} → Wisdom generates prosperity",
                "Wealth through wisdom, education, advisory roles, or spiritual pursuits."
            ))

        # RULE_WLT_003: 5th Lord Strong (Investment Gains)
        h5_lord_dignity = LD(ha, 5)
        if H(ha, 5) >= 65 and not RuleEngine._is_debilitated(h5_lord_dignity):
            evidence = [f"5th house score = {H(ha, 5)}", f"5th lord dignity: {h5_lord_dignity}"]
            conflicts = []
            if rahu_in_house(5): conflicts.append("Rahu in 5th — speculative gains with volatility")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_WLT_003", "Strong 5th House — Investment & Speculative Gains", "Wealth",
                85.0, H(ha, 5), [f"5th house score ≥ 65"],
                evidence, conflicts,
                [L(ha, 5)], [5, 2, 11],
                [y for y in yoga_names if 'Dhana' in y or 'Lakshmi' in y],
                "5th house (Purva Punya, speculation) strong → Gains through investments and intelligence",
                "Profitable investments, speculative gains, and financial intelligence."
            ))

        # RULE_WLT_004: 9th House Strong (Bhagya — Fortune)
        if h9s >= 70:
            evidence = [f"9th house (Bhagya) score = {h9s}", f"9th lord in house {LH(ha, 9)}"]
            conflicts = []
            if RuleEngine._in_trik(LH(ha, 9)): conflicts.append("9th lord in trik reduces fortune manifestation")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_WLT_004", "Strong 9th House — Fortune & Luck", "Wealth",
                90.0, h9s, [f"9th house (Bhagya) score ≥ 70 ({h9s})"],
                evidence, conflicts,
                [L(ha, 9), 'Jupiter'], [9],
                [y for y in yoga_names if 'Lakshmi' in y or 'Raja' in y],
                "9th house (Dharma/Fortune) strong → Cosmic support and fortunate circumstances",
                "Fortune through inheritance, luck, father's support, or righteous actions."
            ))

        # RULE_WLT_005: 2nd Lord in 11th or 11th Lord in 2nd
        if LH(ha, 2) == 11 or LH(ha, 11) == 2:
            evidence = [f"2nd lord {h2_lord} in house {LH(ha, 2)}" if LH(ha, 2) == 11 else f"11th lord {h11_lord} in 2nd house"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_WLT_005", "2nd-11th Lord Exchange — Dhana Yoga", "Wealth",
                92.0, 85.0, ["2nd and 11th lords in mutual exchange"],
                evidence, conflicts,
                [h2_lord, h11_lord], [2, 11],
                [y for y in yoga_names if 'Dhana' in y],
                "2nd lord (wealth) connects with 11th lord (gains) → Classical Dhana Yoga formation",
                "Classical wealth yoga — steady accumulation of material resources and gains."
            ))

        # RULE_WLT_006: Venus Strong in Wealth Houses
        ven_h = get_house_of('Venus')
        ven_dig = dignities.get('Venus', {}).get('dignity_state', 'Neutral')
        if ven_h in [2, 5, 11] and (RuleEngine._is_exalted(ven_dig) or RuleEngine._is_own(ven_dig)):
            evidence = [f"Venus in house {ven_h}", f"Venus dignity: {ven_dig}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_WLT_006", "Strong Venus in Wealth House — Luxury & Comfort", "Wealth",
                88.0, 83.0, [f"Venus in {ven_dig} in house {ven_h}"],
                evidence, conflicts,
                ['Venus'], [ven_h, 7],
                [y for y in yoga_names if 'Malavya' in y or 'Lakshmi' in y],
                f"Venus in wealth house {ven_h} with high dignity → Luxury, art, and material enjoyment",
                "Wealth through arts, luxury goods, beauty industry, or diplomacy."
            ))

        # =====================================================================
        # DOMAIN 4: EDUCATION (5 rules)
        # =====================================================================
        h5_score = H(ha, 5)
        h4_score = H(ha, 4)
        edu_score = round((h5_score + h4_score) / 2.0, 2)
        merc_h = get_house_of('Mercury')
        merc_dig = dignities.get('Mercury', {}).get('dignity_state', 'Neutral')

        # RULE_EDU_001: Strong 5th and 4th Houses
        if edu_score >= 60.0:
            evidence = [f"5th house score = {h5_score}", f"4th house score = {h4_score}"]
            conflicts = []
            if malefic_in_house(5): conflicts.append("Malefic in 5th may create distraction from studies")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_EDU_001", "Strong Academic Houses — Intellectual Acumen", "Education",
                93.0, edu_score, [f"5th+4th combined average ≥ 60 ({edu_score})"],
                evidence, conflicts,
                ['Mercury', 'Jupiter'], [5, 4, 9],
                [y for y in yoga_names if any(kw in y for kw in ['Budhaditya', 'Bhadra', 'Saraswati'])],
                "5th house (intellect/education) + 4th house (knowledge foundation) both strong → Academic excellence",
                "High intellectual capacity, academic success, analytical skill, and scholarly aptitude."
            ))

        # RULE_EDU_002: Mercury Strong
        if (RuleEngine._is_exalted(merc_dig) or RuleEngine._is_own(merc_dig)) and merc_h in [1, 4, 5, 7, 9, 10]:
            evidence = [f"Mercury in {merc_dig}, placed in house {merc_h}"]
            conflicts = []
            if planets.get('Mercury', {}).get('is_combust', False): conflicts.append("Mercury combust reduces analytical clarity")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_EDU_002", "Strong Mercury — Analytical & Communication Excellence", "Education",
                91.0, 86.0, [f"Mercury in {merc_dig} in angular/trine house"],
                evidence, conflicts,
                ['Mercury'], [merc_h, 5],
                [y for y in yoga_names if 'Bhadra' in y or 'Budhaditya' in y],
                f"Mercury (Vidya karaka) in dignity + angular/trine → Superior communication and intelligence",
                "Exceptional analytical ability, communication skill, and academic or technical excellence."
            ))

        # RULE_EDU_003: Jupiter in 5th or Aspects 5th
        if planet_in_house('Jupiter', 5) or jup_aspects(5):
            evidence = ["Jupiter in or aspects 5th house (Vidya Sthana)", f"5th house score: {h5_score}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_EDU_003", "Jupiter Influences 5th — Higher Education & Wisdom", "Education",
                92.0, 87.0, ["Jupiter in or aspects 5th house"],
                evidence, conflicts,
                ['Jupiter'], [5, 9],
                [y for y in yoga_names if 'Hamsa' in y or 'Gajakesari' in y],
                "Jupiter (Guru) in Vidya Bhava (5th) → Higher education, philosophy, and wisdom",
                "University education, higher degrees, teaching, or philosophical pursuits."
            ))

        # RULE_EDU_004: 9th House Strong — Higher Learning
        if h9s >= 65:
            evidence = [f"9th house (Dharma/Guru) score = {h9s}", f"9th lord in house {LH(ha, 9)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_EDU_004", "Strong 9th House — Higher Learning & Philosophy", "Education",
                88.0, h9s, [f"9th house score ≥ 65 ({h9s})"],
                evidence, conflicts,
                [L(ha, 9), 'Jupiter'], [9, 5],
                [y for y in yoga_names if 'Hamsa' in y or 'Saraswati' in y],
                "9th house (Dharma/Higher knowledge) strong → Advanced education, foreign study, philosophical depth",
                "Advanced degrees, research, foreign education, or spiritual learning."
            ))

        # RULE_EDU_005: Mercury-Jupiter Connection
        merc_jup_linked = (merc_h == get_house_of('Jupiter')) or planet_aspects_house('Mercury', get_house_of('Jupiter')) or planet_aspects_house('Jupiter', merc_h)
        if merc_jup_linked:
            evidence = [f"Mercury (house {merc_h}) and Jupiter (house {get_house_of('Jupiter')}) are connected"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_EDU_005", "Mercury-Jupiter Link — Saraswati Yoga Indicator", "Education",
                89.0, 82.0, ["Mercury and Jupiter connected by placement or aspect"],
                evidence, conflicts,
                ['Mercury', 'Jupiter'], [merc_h, get_house_of('Jupiter')],
                [y for y in yoga_names if 'Saraswati' in y or 'Budhaditya' in y],
                "Mercury (intellect) + Jupiter (wisdom) connection → Saraswati Yoga → Profound intellectual gifts",
                "Extraordinary intellectual and communicative abilities — scholarship, writing, or teaching."
            ))

        # =====================================================================
        # DOMAIN 5: HEALTH (5 rules)
        # =====================================================================
        sun_h = get_house_of('Sun')
        sun_dig = dignities.get('Sun', {}).get('dignity_state', 'Neutral')
        h8s = H(ha, 8)
        h12s = H(ha, 12)

        # RULE_HLT_001: Strong Lagna (1st House)
        health_score_1 = round((h1s * 0.6) + ((100 - H(ha, 6)) * 0.2) + ((100 - h8s) * 0.2), 2)
        if h1s >= 60:
            evidence = [f"Lagna score = {h1s}/100", f"6th house score = {H(ha, 6)}", f"8th house score = {h8s}"]
            conflicts = []
            if malefic_in_house(1): conflicts.append("Malefic in Lagna afflicts physical constitution")
            if H(ha, 6) >= 70 and malefic_in_house(6): conflicts.append("Strong 6th house malefics indicate disease vulnerability")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_HLT_001", "Strong Lagna — Physical Vitality & Immunity", "Health",
                88.0, health_score_1, [f"Lagna (1st house) score ≥ 60 ({h1s})"],
                evidence, conflicts,
                [L(ha, 1), 'Sun'], [1, 6],
                [y for y in yoga_names if 'Harsha' in y or 'Vipareeta' in y],
                "1st house (Lagna/Self) strong → Strong constitution, immunity, and recovery ability",
                "Strong immune system, high physical stamina, and quick recovery."
            ))

        # RULE_HLT_002: Sun Strong (Vitality)
        if RuleEngine._is_exalted(sun_dig) or (RuleEngine._is_own(sun_dig) and sun_h in [1, 4, 10]):
            evidence = [f"Sun in {sun_dig}", f"Sun in house {sun_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_HLT_002", "Strong Sun — Vitality & Life Force", "Health",
                87.0, 83.0, [f"Sun in {sun_dig} in house {sun_h}"],
                evidence, conflicts,
                ['Sun'], [1, sun_h],
                [],
                "Sun (Atmakaraka, life force) in peak dignity → Strong vitality and robust constitution",
                "Excellent vitality, strong immune response, and heart health."
            ))

        # RULE_HLT_003: 6th Lord in Trik (Vipareeta — Disease Overcome)
        h6_lord_house = LH(ha, 6)
        if RuleEngine._in_trik(h6_lord_house):
            evidence = [f"6th lord {L(ha, 6)} in trik house {h6_lord_house} (Vipareeta Raja condition)"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_HLT_003", "Vipareeta 6th Lord — Disease Overcome", "Health",
                85.0, 78.0, [f"6th lord in trik house {h6_lord_house}"],
                evidence, conflicts,
                [L(ha, 6)], [6, h6_lord_house],
                [y for y in yoga_names if 'Harsha' in y or 'Vipareeta' in y],
                "6th lord (disease) in trik → Enemy of disease weakened → Recovery and immunity",
                "Tendency to overcome illnesses; strong recovery ability; victory over disease."
            ))

        # RULE_HLT_004: 8th House Afflicted (Longevity Concern)
        if h8s < 40 and malefic_in_house(8):
            mal_8 = [p for p in get_occupants(8) if p in RuleEngine.NATURAL_MALEFICS]
            evidence = [f"8th house score = {h8s} (Afflicted)", f"Malefics in 8th: {mal_8}"]
            conflicts = []
            if jup_aspects(8): conflicts.append("Jupiter's aspect on 8th mitigates longevity concern")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_HLT_004", "Afflicted 8th House — Longevity & Chronic Health Concern", "Health",
                80.0, 100 - h8s, [f"8th house score < 40 with malefic occupants"],
                evidence, conflicts,
                mal_8, [8],
                [],
                "8th house (Ayu/longevity) afflicted by malefics → Chronic health challenges or longevity concern",
                "Attention to chronic conditions; need for health vigilance."
            ))

        # RULE_HLT_005: Lagna Lord Strong
        h1_lord = L(ha, 1)
        h1_lord_dignity = LD(ha, 1)
        if not RuleEngine._is_debilitated(h1_lord_dignity) and RuleEngine._shadbala_strong(shadbala, h1_lord, 300):
            evidence = [f"Lagna lord {h1_lord} in {h1_lord_dignity}", f"Shadbala: {shadbala.get(h1_lord, 0)} Virupas"]
            conflicts = []
            if RuleEngine._in_trik(LH(ha, 1)): conflicts.append(f"Lagna lord in trik house {LH(ha, 1)}")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_HLT_005", "Strong Lagna Lord — Physical Constitution Blessed", "Health",
                86.0, 80.0, [f"Lagna lord {h1_lord} with strong Shadbala and favorable dignity"],
                evidence, conflicts,
                [h1_lord], [1, LH(ha, 1)],
                [],
                f"Lagna lord {h1_lord} (body governor) in favorable dignity + strong Shadbala → Constitution protected",
                "Well-protected physical constitution; resistance to major ailments."
            ))

        # =====================================================================
        # DOMAIN 6: PROPERTY (4 rules)
        # =====================================================================
        h4s = H(ha, 4)
        mars_h = get_house_of('Mars')
        mars_dig = dignities.get('Mars', {}).get('dignity_state', 'Neutral')
        moon_h = get_house_of('Moon')

        # RULE_PRP_001: Strong 4th House
        if h4s >= 65.0:
            evidence = [f"4th house score = {h4s}", f"4th lord {L(ha, 4)} in house {LH(ha, 4)}"]
            conflicts = []
            if rahu_in_house(4): conflicts.append("Rahu in 4th may cause property disputes or foreign living")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PRP_001", "Strong 4th House — Real Estate Prosperity", "Property",
                91.0, h4s, [f"4th house score ≥ 65 ({h4s})"],
                evidence, conflicts,
                ['Mars', 'Venus', L(ha, 4)], [4, 1],
                [y for y in yoga_names if 'Ruchaka' in y or 'Malavya' in y],
                "4th house (Sukha/Property) strong → Fixed assets, real estate, vehicles, and domestic comforts",
                "Acquisition of fixed properties, real estate investments, and home comforts."
            ))

        # RULE_PRP_002: Mars Strong in 4th or 10th (Bhumi Karaka)
        if (RuleEngine._is_exalted(mars_dig) or RuleEngine._is_own(mars_dig)) and mars_h in [4, 10, 1, 7]:
            evidence = [f"Mars (Bhumi karaka) in {mars_dig}", f"Mars in house {mars_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PRP_002", "Strong Mars — Land & Property Acquisition", "Property",
                89.0, 85.0, [f"Mars (land karaka) in {mars_dig} in house {mars_h}"],
                evidence, conflicts,
                ['Mars'], [4, mars_h],
                [y for y in yoga_names if 'Ruchaka' in y],
                "Mars (Bhumi karaka — land lord) in peak dignity → Acquisition of land and real estate",
                "Multiple properties, land ownership, and real estate portfolio growth."
            ))

        # RULE_PRP_003: Moon Strong in 4th (Domestic Bliss)
        if planet_in_house('Moon', 4) and H(ha, 4) >= 55:
            moon_dig = dignities.get('Moon', {}).get('dignity_state', 'Neutral')
            evidence = [f"Moon in 4th house (own/natural placement)", f"Moon dignity: {moon_dig}"]
            conflicts = []
            if malefic_in_house(4): conflicts.append("Malefic in 4th reduces domestic peace")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PRP_003", "Moon in 4th — Domestic Peace & Mother's Blessing", "Property",
                86.0, 80.0, ["Moon placed in 4th house with favorable 4th score"],
                evidence, conflicts,
                ['Moon'], [4],
                [],
                "Moon in 4th (Chandra in Sukha Bhava) → Emotional security, domestic bliss, mother's support",
                "Comfortable home, emotional stability, strong connection to mother, and good domestic life."
            ))

        # RULE_PRP_004: 4th Lord in 1st or 10th
        h4_lord_house = LH(ha, 4)
        if h4_lord_house in [1, 10] and h4s >= 55:
            evidence = [f"4th lord {L(ha, 4)} in house {h4_lord_house}", f"4th house score: {h4s}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PRP_004", "4th Lord in Kendra — Career-Linked Property", "Property",
                84.0, 77.0, [f"4th lord {L(ha, 4)} in house {h4_lord_house} (Kendra)"],
                evidence, conflicts,
                [L(ha, 4)], [4, h4_lord_house],
                [],
                f"4th lord {L(ha, 4)} in prominent house → Property acquired through career/authority",
                "Property and vehicles gained through career achievements."
            ))

        # =====================================================================
        # DOMAIN 7: CHILDREN (4 rules)
        # =====================================================================
        jup_dig_str = dignities.get('Jupiter', {}).get('dignity_state', 'Neutral')
        jup_house = get_house_of('Jupiter')

        # RULE_CHD_001: Strong 5th House
        if h5_score >= 65:
            evidence = [f"5th house score = {h5_score}", f"5th lord {L(ha, 5)} in house {LH(ha, 5)}"]
            conflicts = []
            if ketu_in_house(5): conflicts.append("Ketu in 5th — may indicate fewer children or adoption")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CHD_001", "Strong 5th House — Children & Legacy", "Children",
                88.0, h5_score, [f"5th house score ≥ 65 ({h5_score})"],
                evidence, conflicts,
                ['Jupiter', L(ha, 5)], [5, 9],
                [y for y in yoga_names if 'Raja' in y],
                "5th house (Putra Bhava) strong → Children blessed, intelligent, and successful",
                "Good relationship with children; children achieve success and fame."
            ))

        # RULE_CHD_002: Jupiter in 5th or Aspects 5th
        if planet_in_house('Jupiter', 5) or jup_aspects(5):
            evidence = ["Jupiter in or aspects 5th house (Putra karaka)", f"Jupiter: {jup_dig_str}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CHD_002", "Jupiter Blesses 5th — Children's Prosperity", "Children",
                91.0, 86.0, ["Jupiter in or aspects 5th (Putra Bhava)"],
                evidence, conflicts,
                ['Jupiter'], [5],
                [y for y in yoga_names if 'Hamsa' in y or 'Gajakesari' in y],
                "Jupiter (Putra karaka) in or aspects 5th → Children's wellbeing and intellect blessed",
                "Children are intelligent, virtuous, and achieve high status."
            ))

        # RULE_CHD_003: 9th House Strong (Bhagya for children)
        if h9s >= 65 and H(ha, 5) >= 55:
            evidence = [f"9th house score = {h9s}", f"5th house score = {H(ha, 5)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CHD_003", "9th-5th House Link — Blessed Offspring", "Children",
                86.0, (h9s + H(ha, 5)) / 2, ["9th house ≥ 65 and 5th house ≥ 55"],
                evidence, conflicts,
                [L(ha, 9), 'Jupiter'], [9, 5],
                [],
                "9th house (Bhagya, father) + 5th house (children) both strong → Intergenerational blessing",
                "Family legacy passed forward; children carry the family name with pride."
            ))

        # RULE_CHD_004: Malefic in 5th (Challenge to Children)
        if malefic_in_house(5) and h5_score < 50:
            mal_5 = [p for p in get_occupants(5) if p in RuleEngine.NATURAL_MALEFICS]
            evidence = [f"Malefics {mal_5} in 5th house", f"5th house score: {h5_score}"]
            conflicts = []
            if jup_aspects(5): conflicts.append("Jupiter's aspect mitigates difficulty with children")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_CHD_004", "Malefic in 5th — Children Challenges", "Children",
                78.0, 100 - h5_score, [f"Malefics {mal_5} in 5th with score < 50"],
                evidence, conflicts,
                mal_5, [5],
                [],
                f"Malefics {mal_5} in Putra Bhava → Delay, difficulty, or challenges related to children",
                "Children may face health challenges or there may be delayed parenthood."
            ))

        # =====================================================================
        # DOMAIN 8: SIBLINGS (3 rules)
        # =====================================================================
        h3s = H(ha, 3)
        h3_lord = L(ha, 3)
        h11_score = H(ha, 11)
        mars_dig_sibling = dignities.get('Mars', {}).get('dignity_state', 'Neutral')

        # RULE_SIB_001: Strong 3rd House
        if h3s >= 60:
            evidence = [f"3rd house score = {h3s}", f"3rd lord {h3_lord} in house {LH(ha, 3)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_SIB_001", "Strong 3rd House — Sibling Harmony", "Siblings",
                84.0, h3s, [f"3rd house score ≥ 60 ({h3s})"],
                evidence, conflicts,
                [h3_lord, 'Mars'], [3, 11],
                [],
                "3rd house (Sahaja/Siblings) strong → Supportive siblings, courage, and communication",
                "Good sibling relationships, mutual support, and cooperative endeavors."
            ))

        # RULE_SIB_002: Mars Strong (Courage & Sibling Power)
        if (RuleEngine._is_exalted(mars_dig_sibling) or RuleEngine._is_own(mars_dig_sibling)) and mars_h in [3, 1, 10, 11]:
            evidence = [f"Mars (Sahaja karaka) in {mars_dig_sibling}", f"Mars in house {mars_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_SIB_002", "Strong Mars — Courageous Siblings", "Siblings",
                83.0, 78.0, [f"Mars in {mars_dig_sibling} in house {mars_h}"],
                evidence, conflicts,
                ['Mars'], [3, mars_h],
                [y for y in yoga_names if 'Ruchaka' in y],
                "Mars (Sahaja karaka) in peak dignity + 3rd house placement → Courageous, assertive siblings",
                "Courageous and successful siblings who support and inspire."
            ))

        # RULE_SIB_003: 11th Strong (Elder Sibling Success)
        if h11_score >= 65:
            evidence = [f"11th house score = {h11_score}", f"11th lord in house {LH(ha, 11)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_SIB_003", "Strong 11th House — Gains Through Siblings", "Siblings",
                82.0, h11_score, [f"11th house score ≥ 65 ({h11_score})"],
                evidence, conflicts,
                [L(ha, 11)], [11, 3],
                [],
                "11th house (gains, elder siblings) strong → Elder siblings prosperous and helpful",
                "Gains and support from elder siblings; mutual prosperity."
            ))

        # =====================================================================
        # DOMAIN 9: PARENTS (4 rules)
        # =====================================================================
        h4_score_p = H(ha, 4)
        h9_score_p = H(ha, 9)

        # RULE_PAR_001: Strong 4th House — Mother
        if h4_score_p >= 65:
            evidence = [f"4th house (Matru Bhava) score = {h4_score_p}", f"Moon in house {moon_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PAR_001", "Strong 4th House — Mother's Blessing", "Parents",
                87.0, h4_score_p, [f"4th house ≥ 65 ({h4_score_p})"],
                evidence, conflicts,
                ['Moon', L(ha, 4)], [4],
                [],
                "4th house (Matru Bhava) strong → Long-lived, prosperous, and supportive mother",
                "Blessed relationship with mother; mother's guidance and support throughout life."
            ))

        # RULE_PAR_002: Strong 9th House — Father
        if h9_score_p >= 65:
            evidence = [f"9th house (Pitru Bhava) score = {h9_score_p}", f"Sun in house {sun_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PAR_002", "Strong 9th House — Father's Fortune", "Parents",
                87.0, h9_score_p, [f"9th house ≥ 65 ({h9_score_p})"],
                evidence, conflicts,
                ['Sun', L(ha, 9)], [9],
                [],
                "9th house (Pitru Bhava) strong → Prosperous, long-lived father and ancestral blessings",
                "Father's fortune and blessings guide the native's life path."
            ))

        # RULE_PAR_003: Sun Strong — Father's Status
        if (RuleEngine._is_exalted(sun_dig) or RuleEngine._is_own(sun_dig)) and sun_h in [1, 9, 10, 5]:
            evidence = [f"Sun in {sun_dig}, house {sun_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PAR_003", "Strong Sun — Distinguished Father", "Parents",
                85.0, 80.0, [f"Sun (Pitrukaraka) in {sun_dig}"],
                evidence, conflicts,
                ['Sun'], [9, sun_h],
                [],
                "Sun (Pitrukaraka) in peak dignity → Father is distinguished, authoritative, and successful",
                "Father holds a position of authority or social distinction."
            ))

        # RULE_PAR_004: 10th and 9th Both Strong (Family Legacy)
        if H(ha, 10) >= 65 and h9s >= 65:
            evidence = [f"10th house = {H(ha, 10)}", f"9th house = {h9s}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_PAR_004", "9th-10th Strength — Family Legacy & Ancestral Honor", "Parents",
                88.0, (H(ha, 10) + h9s) / 2, ["9th and 10th houses both ≥ 65"],
                evidence, conflicts,
                [L(ha, 9), L(ha, 10)], [9, 10],
                [y for y in yoga_names if 'Raja' in y],
                "9th (father/lineage) + 10th (career/authority) both strong → Continuing family legacy",
                "Native carries forward a distinguished family tradition or ancestral legacy."
            ))

        # =====================================================================
        # DOMAIN 10: FOREIGN TRAVEL (4 rules)
        # =====================================================================
        h12_score = H(ha, 12)
        h9_score_ft = H(ha, 9)
        h3_score_ft = H(ha, 3)
        rahu_house = get_house_of('Rahu')

        # RULE_FRN_001: 12th House Strong (Foreign Residence)
        if h12_score >= 60:
            evidence = [f"12th house score = {h12_score}", f"12th lord in house {LH(ha, 12)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_FRN_001", "Strong 12th House — Foreign Residence", "Foreign Travel",
                85.0, h12_score, [f"12th house score ≥ 60 ({h12_score})"],
                evidence, conflicts,
                [L(ha, 12), 'Rahu'], [12, 9],
                [y for y in yoga_names if 'Vimala' in y],
                "12th house (Vyaya/Foreign lands) strong → Long foreign stays, international success",
                "Long-term residence abroad, international career, or foreign travel opportunities."
            ))

        # RULE_FRN_002: Rahu in 9th, 12th, or 3rd (Foreign Impulse)
        if rahu_house in [3, 9, 12]:
            evidence = [f"Rahu in house {rahu_house} (foreign-travel-linked house)"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_FRN_002", "Rahu in Travel House — Foreign Opportunity", "Foreign Travel",
                83.0, 76.0, [f"Rahu in house {rahu_house} (foreign-linked)"],
                evidence, conflicts,
                ['Rahu'], [rahu_house],
                [],
                f"Rahu in {rahu_house}th house → Strong pull toward foreign lands and unconventional journeys",
                "Frequent travel, foreign business, or life-changing experiences abroad."
            ))

        # RULE_FRN_003: 12th Lord in 1st, 9th, or 3rd
        h12_lord_house = LH(ha, 12)
        if h12_lord_house in [1, 9, 3]:
            evidence = [f"12th lord {L(ha, 12)} in house {h12_lord_house}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_FRN_003", "12th Lord in Travel House — Abroad-Oriented Life", "Foreign Travel",
                82.0, 75.0, [f"12th lord {L(ha, 12)} in house {h12_lord_house}"],
                evidence, conflicts,
                [L(ha, 12)], [12, h12_lord_house],
                [],
                f"12th lord in house {h12_lord_house} → Natural orientation toward foreign lands",
                "Natural tendency toward international living, foreign education, or long journeys."
            ))

        # RULE_FRN_004: 9th and 12th Combined (Immigration/Settlement)
        if h9_score_ft >= 60 and h12_score >= 60:
            evidence = [f"9th house = {h9_score_ft}", f"12th house = {h12_score}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_FRN_004", "9th-12th Combination — Immigration & Settlement Abroad", "Foreign Travel",
                88.0, (h9_score_ft + h12_score) / 2, ["9th and 12th houses both ≥ 60"],
                evidence, conflicts,
                [L(ha, 9), L(ha, 12)], [9, 12],
                [],
                "9th (long journeys) + 12th (foreign lands) both strong → Permanent foreign settlement possible",
                "High probability of immigration, foreign residency, or long-term international career."
            ))

        # =====================================================================
        # DOMAIN 11: SPIRITUALITY (4 rules)
        # =====================================================================
        ketu_h = get_house_of('Ketu')

        # RULE_SPI_001: 9th-12th Combination
        spi_score = round((h9s + h12s) / 2.0, 2)
        if spi_score >= 60.0:
            evidence = [f"9th house score = {h9s}", f"12th house score = {h12s}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_SPI_001", "Spiritual Inclination — 9th & 12th Alignment", "Spirituality",
                89.0, spi_score, [f"9th+12th average ≥ 60 ({spi_score})"],
                evidence, conflicts,
                ['Jupiter', 'Ketu'], [9, 12, 5],
                [y for y in yoga_names if any(kw in y for kw in ['Hamsa', 'Vimala', 'Kalasarpa'])],
                "9th (dharma) + 12th (moksha/liberation) → Spiritual orientation and higher knowledge",
                "Deep reverence for higher philosophy, spiritual practices, and karmic wisdom."
            ))

        # RULE_SPI_002: Ketu in 9th, 12th, or 1st
        if ketu_h in [1, 9, 12, 5]:
            evidence = [f"Ketu (Moksha karaka) in house {ketu_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_SPI_002", "Ketu in Moksha House — Spiritual Liberation", "Spirituality",
                88.0, 82.0, [f"Ketu in house {ketu_h} (moksha-linked)"],
                evidence, conflicts,
                ['Ketu'], [ketu_h, 12],
                [y for y in yoga_names if 'Kalasarpa' in y],
                "Ketu (Moksha karaka) in liberation/dharma house → Natural pull toward spirituality and inner wisdom",
                "Spiritual practices, meditation, and liberation from material attachment."
            ))

        # RULE_SPI_003: Jupiter Strong in 9th or 5th
        if planet_in_house('Jupiter', 9) or planet_in_house('Jupiter', 5):
            jup_h_spi = get_house_of('Jupiter')
            evidence = [f"Jupiter in house {jup_h_spi} (dharma/wisdom house)", f"Jupiter: {jup_dig_str}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_SPI_003", "Jupiter in Dharma/Wisdom House — Guru Blessing", "Spirituality",
                92.0, 88.0, [f"Jupiter in house {jup_h_spi}"],
                evidence, conflicts,
                ['Jupiter'], [jup_h_spi],
                [y for y in yoga_names if 'Hamsa' in y or 'Gajakesari' in y],
                "Jupiter in dharma house → Natural wisdom, spiritual teaching ability, and philosophical depth",
                "Deep spiritual wisdom, teaching ability, and connection to gurus and higher knowledge."
            ))

        # RULE_SPI_004: 5th Lord in 9th or 9th Lord in 5th (Purva Punya)
        if LH(ha, 5) == 9 or LH(ha, 9) == 5:
            evidence = [f"5th lord {L(ha, 5)} in house {LH(ha, 5)} OR 9th lord {L(ha, 9)} in house {LH(ha, 9)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_SPI_004", "5th-9th Lord Exchange — Purva Punya Yoga", "Spirituality",
                91.0, 86.0, ["5th and 9th lords in exchange or connection"],
                evidence, conflicts,
                [L(ha, 5), L(ha, 9)], [5, 9],
                [y for y in yoga_names if 'Hamsa' in y or 'Raja' in y],
                "5th (purva punya/past merit) connects 9th (dharma) → Exceptional spiritual merit from past lives",
                "Strong spiritual inclination rooted in past life merit; natural spiritual authority."
            ))

        # =====================================================================
        # DOMAIN 12: LITIGATION (3 rules)
        # =====================================================================
        h6s = H(ha, 6)
        h8s_lit = H(ha, 8)
        rahu_h_lit = get_house_of('Rahu')

        # RULE_LIT_001: 6th House + Mars/Rahu Malefic Combination
        if h6s >= 65 and (malefic_in_house(6) or malefic_in_house(1)):
            evidence = [f"6th house score = {h6s}", "Malefic influence on 6th/Lagna"]
            conflicts = []
            if jup_aspects(6): conflicts.append("Jupiter aspects 6th — legal wisdom and protection")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_LIT_001", "Strong 6th with Malefic — Litigation & Conflict", "Litigation",
                80.0, h6s, [f"6th house ≥ 65 with malefic influence"],
                evidence, conflicts,
                [L(ha, 6), 'Mars', 'Rahu'], [6],
                [],
                "6th house (Shatru/enemies) strong + malefic → Disputes, lawsuits, or conflicts",
                "Legal disputes or conflicts are possible; need for legal vigilance."
            ))

        # RULE_LIT_002: Rahu in 6th or 7th (Legal Complications)
        if rahu_h_lit in [6, 7]:
            evidence = [f"Rahu in house {rahu_h_lit}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_LIT_002", "Rahu in 6th/7th — Legal Entanglements", "Litigation",
                78.0, 72.0, [f"Rahu in house {rahu_h_lit}"],
                evidence, conflicts,
                ['Rahu'], [6, 7],
                [],
                f"Rahu in {rahu_h_lit}th house → Unconventional disputes or legal complications",
                "Unexpected legal entanglements or disputes with hidden enemies."
            ))

        # RULE_LIT_003: 6th Lord Strong (Victory in Litigation)
        h6_lord = L(ha, 6)
        if RuleEngine._shadbala_strong(shadbala, h6_lord, 350) and not RuleEngine._in_trik(LH(ha, 6)):
            evidence = [f"6th lord {h6_lord} has strong Shadbala {shadbala.get(h6_lord, 0)}", f"6th lord in house {LH(ha, 6)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_LIT_003", "Strong 6th Lord — Victory Over Enemies", "Litigation",
                84.0, 79.0, [f"6th lord {h6_lord} has strong Shadbala"],
                evidence, conflicts,
                [h6_lord], [6],
                [y for y in yoga_names if 'Harsha' in y or 'Vipareeta' in y],
                f"6th lord {h6_lord} strong → Enemy/opposition weakened → Victory in disputes and litigation",
                "Victory over enemies and legal opponents; triumph in disputes."
            ))

        # =====================================================================
        # DOMAIN 13: BUSINESS (4 rules)
        # =====================================================================

        # RULE_BUS_001: 7th+11th Commercial Nexus
        if h7s >= 60.0 and h11_score >= 60.0:
            evidence = [f"7th house score = {h7s}", f"11th house score = {h11_score}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_BUS_001", "Commercial Enterprise — Trade Success", "Business",
                87.0, round((h7s + h11_score) / 2.0, 2), ["7th ≥ 60 and 11th ≥ 60"],
                evidence, conflicts,
                ['Mercury', 'Venus'], [7, 11, 3],
                [y for y in yoga_names if any(kw in y for kw in ['Bhadra', 'Chandra Mangala'])],
                "7th (partnerships) + 11th (gains) both strong → Successful commercial enterprise",
                "Profitable business operations, strategic partnerships, and market gains."
            ))

        # RULE_BUS_002: Mercury Strong in 7th or 10th
        if (RuleEngine._is_exalted(merc_dig) or RuleEngine._is_own(merc_dig)) and merc_h in [7, 10, 2, 11]:
            evidence = [f"Mercury in {merc_dig}, house {merc_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_BUS_002", "Strong Mercury in Business House — Trade Intelligence", "Business",
                88.0, 83.0, [f"Mercury in {merc_dig} in house {merc_h}"],
                evidence, conflicts,
                ['Mercury'], [merc_h, 7, 11],
                [y for y in yoga_names if 'Bhadra' in y or 'Budhaditya' in y],
                f"Mercury (Vanika karaka/trade) in {merc_dig} + business house → Commercial acumen",
                "Sharp business mind, trading ability, and commercial success."
            ))

        # RULE_BUS_003: 3rd House Strong (Self-Employment Courage)
        if h3s >= 60:
            evidence = [f"3rd house (self-effort) score = {h3s}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_BUS_003", "Strong 3rd House — Entrepreneurial Courage", "Business",
                82.0, h3s, [f"3rd house score ≥ 60 ({h3s})"],
                evidence, conflicts,
                [L(ha, 3), 'Mars'], [3, 7, 11],
                [],
                "3rd house (Parakrama/self-effort, younger siblings) strong → Entrepreneurial boldness",
                "Independent business ventures, entrepreneurial spirit, and self-made success."
            ))

        # RULE_BUS_004: 7th Lord in 11th or 11th Lord in 7th
        if LH(ha, 7) == 11 or LH(ha, 11) == 7:
            evidence = [f"7th lord {h7_lord} in house {LH(ha, 7)} OR 11th lord in 7th"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_BUS_004", "7th-11th Lord Exchange — Business Partnership Gains", "Business",
                89.0, 84.0, ["7th and 11th lords in exchange"],
                evidence, conflicts,
                [h7_lord, L(ha, 11)], [7, 11],
                [y for y in yoga_names if 'Dhana' in y],
                "7th (partnership) lord exchanges with 11th (gains) → Business partnerships bring great gains",
                "Highly profitable business partnerships and trade alliances."
            ))

        # =====================================================================
        # DOMAIN 14: GOVERNMENT SERVICE (3 rules)
        # =====================================================================

        # RULE_GOV_001: Sun Strong in 10th or 1st
        if sun_h in [10, 1, 9] and (RuleEngine._is_exalted(sun_dig) or RuleEngine._is_own(sun_dig) or h10s >= 70):
            evidence = [f"Sun in house {sun_h}", f"Sun dignity: {sun_dig}", f"10th house: {h10s}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_GOV_001", "Sun in Authority House — Government & Leadership", "Government",
                89.0, 84.0, [f"Sun in house {sun_h} with favorable dignity"],
                evidence, conflicts,
                ['Sun'], [10, sun_h],
                [y for y in yoga_names if 'Raja' in y],
                f"Sun (Rajya karaka) in house {sun_h} → Natural authority; government connections and positions",
                "Career in government, administration, or positions of public authority."
            ))

        # RULE_GOV_002: Mars in 10th (Military/Police)
        if planet_in_house('Mars', 10) and H(ha, 10) >= 55:
            evidence = ["Mars in 10th house", f"Mars dignity: {mars_dig}", f"10th house score: {H(ha, 10)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_GOV_002", "Mars in 10th — Military, Police & Command", "Government",
                86.0, 81.0, ["Mars in 10th house with favorable 10th score"],
                evidence, conflicts,
                ['Mars'], [10],
                [y for y in yoga_names if 'Ruchaka' in y],
                "Mars in 10th (Digbala) → Military command, police, or executive government authority",
                "Career in defense, police, fire service, or executive government roles."
            ))

        # RULE_GOV_003: Yogakaraka Influences 10th
        yogakaraka_gov = functional.get('yogakaraka', None)
        if yogakaraka_gov and planet_aspects_house(yogakaraka_gov, 10):
            evidence = [f"Yogakaraka {yogakaraka_gov} aspects 10th house"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_GOV_003", "Yogakaraka Aspects 10th — Government Recognition", "Government",
                91.0, 87.0, [f"Yogakaraka {yogakaraka_gov} aspects 10th"],
                evidence, conflicts,
                [yogakaraka_gov], [10],
                [y for y in yoga_names if 'Raja' in y or 'Mahapurusha' in y],
                f"Yogakaraka {yogakaraka_gov} aspects career house → Highest level of government recognition",
                "Government recognition, awards, titles, or high public office."
            ))

        # =====================================================================
        # DOMAIN 15: FAME & RECOGNITION (3 rules)
        # =====================================================================

        # RULE_FAM_001: 10th+11th Combined (Fame + Gains)
        if H(ha, 10) >= 65 and H(ha, 11) >= 65:
            evidence = [f"10th house = {H(ha, 10)}", f"11th house = {H(ha, 11)}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_FAM_001", "10th-11th Combination — Fame & Mass Recognition", "Fame",
                90.0, (H(ha, 10) + H(ha, 11)) / 2, ["10th and 11th houses both ≥ 65"],
                evidence, conflicts,
                [L(ha, 10), L(ha, 11)], [10, 11],
                [y for y in yoga_names if 'Raja' in y or 'Gajakesari' in y],
                "10th (authority/reputation) + 11th (mass gains/social network) → Fame and public recognition",
                "Wide public recognition, fame, and mass following."
            ))

        # RULE_FAM_002: Raja Yoga Active
        if RuleEngine._yoga_present(yoga_names, ['Raja', 'Mahapurusha', 'Hamsa', 'Ruchaka', 'Malavya', 'Bhadra', 'Sasa']):
            top_raja = next((y for y in yoga_names if any(kw in y for kw in ['Raja', 'Mahapurusha', 'Hamsa', 'Ruchaka', 'Malavya', 'Bhadra', 'Sasa'])), '')
            evidence = [f"Raja/Mahapurusha Yoga active: {top_raja}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_FAM_002", "Raja/Mahapurusha Yoga — Exceptional Fame", "Fame",
                94.0, 90.0, [f"Active Raja or Mahapurusha Yoga: {top_raja}"],
                evidence, conflicts,
                [top_planet], [10, 1],
                [top_raja],
                f"Active {top_raja} → Exceptional reputation and fame exceeding ordinary achievement",
                "Exceptional public reputation; fame that extends beyond normal professional achievement."
            ))

        # RULE_FAM_003: Sun-Jupiter Connection
        sun_jup_linked = (sun_h == get_house_of('Jupiter')) or planet_aspects_house('Jupiter', sun_h) or planet_aspects_house('Sun', get_house_of('Jupiter'))
        if sun_jup_linked and H(ha, 10) >= 55:
            evidence = [f"Sun (house {sun_h}) connected with Jupiter (house {get_house_of('Jupiter')})"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_FAM_003", "Sun-Jupiter Connection — Honorable Fame", "Fame",
                86.0, 80.0, ["Sun and Jupiter connected through placement or aspect"],
                evidence, conflicts,
                ['Sun', 'Jupiter'], [sun_h, get_house_of('Jupiter'), 10],
                [y for y in yoga_names if 'Hamsa' in y or 'Raja' in y],
                "Sun (authority/ego) + Jupiter (wisdom/dharma) → Fame built on ethical authority and wisdom",
                "Fame built on ethical leadership, wisdom, and righteous authority."
            ))

        # =====================================================================
        # DOMAIN 16: LONGEVITY (3 rules)
        # =====================================================================

        # RULE_LON_001: 8th House Reasonably Strong
        h8_score = H(ha, 8)
        if h8_score >= 55:
            evidence = [f"8th house (Ayu Bhava) score = {h8_score}", f"8th lord {L(ha, 8)} in house {LH(ha, 8)}"]
            conflicts = []
            if malefic_in_house(8): conflicts.append("Malefic in 8th may create health challenges")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_LON_001", "8th House Adequate — Life Span Supported", "Longevity",
                83.0, h8_score, [f"8th house score ≥ 55 ({h8_score})"],
                evidence, conflicts,
                [L(ha, 8), 'Saturn'], [8],
                [],
                "8th house (Ayu/longevity) reasonably strong → Life span supported",
                "Good life expectancy; ability to withstand major health crises."
            ))

        # RULE_LON_002: Saturn Strong (Longevity Karaka)
        sat_dig = dignities.get('Saturn', {}).get('dignity_state', 'Neutral')
        sat_h = get_house_of('Saturn')
        if (RuleEngine._is_exalted(sat_dig) or RuleEngine._is_own(sat_dig)) and not RuleEngine._in_trik(sat_h):
            evidence = [f"Saturn (Ayu karaka) in {sat_dig}", f"Saturn in house {sat_h}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_LON_002", "Strong Saturn — Long Life & Endurance", "Longevity",
                87.0, 83.0, [f"Saturn in {sat_dig} outside trik houses"],
                evidence, conflicts,
                ['Saturn'], [sat_h, 8],
                [y for y in yoga_names if 'Sasa' in y],
                "Saturn (Ayu karaka — longevity lord) in peak dignity → Strong life force and endurance",
                "Long, healthy life with strong physical endurance and resistance to disease."
            ))

        # RULE_LON_003: Lagna Lord and 8th Lord Both Outside Trik
        l1_lh = LH(ha, 1)
        l8_lh = LH(ha, 8)
        if not RuleEngine._in_trik(l1_lh) and not RuleEngine._in_trik(l8_lh):
            evidence = [f"Lagna lord {L(ha, 1)} in house {l1_lh} (not trik)", f"8th lord {L(ha, 8)} in house {l8_lh} (not trik)"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_LON_003", "Lagna + 8th Lords in Auspicious Positions — Protected Life", "Longevity",
                85.0, 80.0, ["Lagna and 8th lords both outside trik houses"],
                evidence, conflicts,
                [L(ha, 1), L(ha, 8)], [1, 8, l1_lh, l8_lh],
                [],
                "Lagna lord (self) + 8th lord (longevity) in auspicious positions → Life well-protected",
                "Strong life protection; longevity well-supported by chart."
            ))

        # =====================================================================
        # DOMAIN 17: ACCIDENTS & SUDDEN EVENTS (3 rules)
        # =====================================================================

        # RULE_ACC_001: 8th House Heavily Afflicted
        if h8_score < 35 and malefic_in_house(8):
            mal_8 = [p for p in get_occupants(8) if p in RuleEngine.NATURAL_MALEFICS]
            evidence = [f"8th house score = {h8_score} (heavily afflicted)", f"Malefics: {mal_8}"]
            conflicts = []
            if jup_aspects(8): conflicts.append("Jupiter's aspect mitigates accident potential")
            rule_matches.append(RuleEngine._make_rule(
                "RULE_ACC_001", "Heavily Afflicted 8th — Accident Vulnerability", "Accidents",
                75.0, 100 - h8_score, [f"8th house score < 35 with malefics {mal_8}"],
                evidence, conflicts,
                mal_8, [8],
                [],
                f"8th house (sudden events/accidents) with malefics {mal_8} → Heightened accident vulnerability",
                "Need for caution regarding accidents, surgeries, or sudden physical events."
            ))

        # RULE_ACC_002: Mars-Rahu Conjunction
        mars_rahu_same = get_house_of('Mars') == get_house_of('Rahu')
        if mars_rahu_same:
            shared_house = get_house_of('Mars')
            evidence = [f"Mars and Rahu conjunct in house {shared_house}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_ACC_002", "Mars-Rahu Conjunction — Explosive Energy & Accident Risk", "Accidents",
                76.0, 72.0, ["Mars and Rahu conjunct in same house"],
                evidence, conflicts,
                ['Mars', 'Rahu'], [shared_house, 8, 6],
                [],
                "Mars (aggression/fire) + Rahu (chaos/obsession) → Sudden explosive events and accident potential",
                "Heightened accident risk during Mars or Rahu dashas; need for physical caution."
            ))

        # RULE_ACC_003: 6th + 8th Dual Affliction
        if h6s < 40 and h8_score < 40:
            evidence = [f"6th house score = {h6s}", f"8th house score = {h8_score}"]
            conflicts = []
            rule_matches.append(RuleEngine._make_rule(
                "RULE_ACC_003", "Dual Trik Affliction — Health & Accident Caution", "Accidents",
                78.0, (100 - h6s + 100 - h8_score) / 2, ["6th and 8th houses both below 40"],
                evidence, conflicts,
                [L(ha, 6), L(ha, 8)], [6, 8],
                [],
                "6th (disease/enemies) + 8th (accidents/sudden) both weak → Compounded health/accident vulnerability",
                "Heightened vulnerability to both health challenges and sudden accidents."
            ))

        return rule_matches
