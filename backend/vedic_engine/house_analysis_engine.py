# -*- coding: utf-8 -*-
"""
House Analysis Engine v2.0.
Performs quantitative and qualitative evaluations for all 12 houses.
New: net_benefic_score, net_malefic_score, net_influence_score, is_afflicted, is_protected,
strongest_influence, weakest_influence, benefic/malefic counts by type, house_type classification.
"""

class HouseAnalysisEngine:
    SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    NATURAL_BENEFICS = ['Jupiter', 'Venus', 'Mercury', 'Moon']
    NATURAL_MALEFICS = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']

    # House type classifications
    KENDRA_HOUSES = [1, 4, 7, 10]
    TRIKONA_HOUSES = [1, 5, 9]
    UPACHAYA_HOUSES = [3, 6, 10, 11]
    TRIK_HOUSES = [6, 8, 12]
    DHARMA_HOUSES = [1, 5, 9]
    ARTHA_HOUSES = [2, 6, 10]
    KAMA_HOUSES = [3, 7, 11]
    MOKSHA_HOUSES = [4, 8, 12]

    # Benefic weight per planet (for influence scoring)
    BENEFIC_WEIGHTS = {
        'Jupiter': 10.0, 'Venus': 9.0, 'Mercury': 7.0, 'Moon': 6.0
    }
    MALEFIC_WEIGHTS = {
        'Saturn': 9.0, 'Mars': 8.0, 'Rahu': 7.5, 'Ketu': 7.0, 'Sun': 4.0
    }

    @staticmethod
    def get_house_type(h: int) -> str:
        types = []
        if h in HouseAnalysisEngine.KENDRA_HOUSES:
            types.append('Kendra')
        if h in HouseAnalysisEngine.TRIKONA_HOUSES:
            types.append('Trikona')
        if h in HouseAnalysisEngine.UPACHAYA_HOUSES:
            types.append('Upachaya')
        if h in HouseAnalysisEngine.TRIK_HOUSES:
            types.append('Trik')
        return '/'.join(types) if types else 'Neutral'

    @staticmethod
    def analyze_houses(master_obj: dict) -> dict:
        houses_analysis = {}
        
        houses_info = master_obj.get('houses', {})
        asc_sign_idx = int(houses_info.get('ascendant_sidereal_lon', 0.0) / 30.0) % 12
        planets_data = master_obj.get('planets', {})
        dignities = master_obj.get('dignity', {})
        aspects_data = master_obj.get('planetary_aspects', [])
        shadbala_data = master_obj.get('shadbala', {})

        # Group occupants by house (1-12)
        occupants_by_house = {h: [] for h in range(1, 13)}
        for p, d in planets_data.items():
            s_idx = d.get('sign_index', 0)
            h_num = ((s_idx - asc_sign_idx + 12) % 12) + 1
            occupants_by_house[h_num].append(p)

        # Aspects by target house — only count effective aspects
        aspects_by_house = {h: [] for h in range(1, 13)}
        for asp in aspects_data:
            t_house = asp.get('target_house', 1)
            # Include all aspects but mark effectiveness
            aspects_by_house[t_house].append({
                'planet': asp.get('aspecting_planet'),
                'is_effective': asp.get('is_effective', True),
                'effective_strength': asp.get('effective_strength', asp.get('strength_percentage', 50.0))
            })

        for h in range(1, 13):
            sign_idx = (asc_sign_idx + h - 1) % 12
            lord = HouseAnalysisEngine.SIGN_LORDS[sign_idx]
            sign_name = HouseAnalysisEngine.SIGN_NAMES[sign_idx]  # FIX: use actual sign name
            
            lord_data = planets_data.get(lord, {})
            lord_sign_idx = lord_data.get('sign_index', 0)
            lord_house = ((lord_sign_idx - asc_sign_idx + 12) % 12) + 1
            lord_dignity = dignities.get(lord, {}).get('dignity_state', 'Neutral')
            lord_shadbala = shadbala_data.get(lord, 300.0)

            occupants = occupants_by_house[h]
            aspect_entries = aspects_by_house[h]
            aspecting_planets = [e['planet'] for e in aspect_entries]
            effective_aspecting = [e['planet'] for e in aspect_entries if e.get('is_effective', True)]

            # All influences (occupants + all aspecting planets)
            all_influences = occupants + aspecting_planets
            
            benefic_occupants = [p for p in occupants if p in HouseAnalysisEngine.NATURAL_BENEFICS]
            malefic_occupants = [p for p in occupants if p in HouseAnalysisEngine.NATURAL_MALEFICS]
            benefic_aspecting = [p for p in effective_aspecting if p in HouseAnalysisEngine.NATURAL_BENEFICS]
            malefic_aspecting = [p for p in effective_aspecting if p in HouseAnalysisEngine.NATURAL_MALEFICS]

            # Weighted influence scores
            benefic_influences = benefic_occupants + benefic_aspecting
            malefic_influences = malefic_occupants + malefic_aspecting

            net_benefic_score = sum(HouseAnalysisEngine.BENEFIC_WEIGHTS.get(p, 5.0) for p in benefic_influences)
            net_malefic_score = sum(HouseAnalysisEngine.MALEFIC_WEIGHTS.get(p, 5.0) for p in malefic_influences)
            net_influence_score = round(net_benefic_score - net_malefic_score, 2)

            # Strongest and weakest influence
            all_weighted = {}
            for p in occupants + effective_aspecting:
                if p in HouseAnalysisEngine.BENEFIC_WEIGHTS:
                    all_weighted[p] = HouseAnalysisEngine.BENEFIC_WEIGHTS[p]
                elif p in HouseAnalysisEngine.MALEFIC_WEIGHTS:
                    all_weighted[p] = -HouseAnalysisEngine.MALEFIC_WEIGHTS[p]
            strongest_influence = max(all_weighted, key=lambda x: all_weighted[x]) if all_weighted else None
            weakest_influence = min(all_weighted, key=lambda x: all_weighted[x]) if all_weighted else None

            # House Score Calculation
            score = 50.0
            if "Exalted" in lord_dignity or "Moolatrikona" in lord_dignity:
                score += 25.0
            elif "Own Sign" in lord_dignity or "Friend" in lord_dignity or "Great Friend" in lord_dignity:
                score += 15.0
            elif "Debilitated" in lord_dignity or "Great Enemy" in lord_dignity:
                score -= 20.0
            elif "Enemy" in lord_dignity:
                score -= 12.0

            if lord_house in [1, 4, 7, 10, 5, 9]:
                score += 15.0
            elif lord_house in [6, 8, 12]:
                score -= 15.0

            score += len(benefic_occupants) * 10.0
            score += len(benefic_aspecting) * 6.0
            score -= len(malefic_occupants) * 9.0
            score -= len(malefic_aspecting) * 5.0

            final_score = min(100.0, max(0.0, round(score, 2)))

            # Afflicted/Protected determination
            is_afflicted = (net_malefic_score > net_benefic_score + 5.0) or (final_score < 40.0)
            is_protected = (net_benefic_score > net_malefic_score + 5.0) or ('Jupiter' in benefic_influences)

            house_type = HouseAnalysisEngine.get_house_type(h)

            houses_analysis[f"house_{h}"] = {
                # ── Backward-compatible fields ──
                "house_number": h,
                "sign": sign_name,          # FIX: was showing lord name, now shows actual sign name
                "sign_index": sign_idx,
                "house_lord": lord,
                "lord_location_house": lord_house,
                "lord_dignity": lord_dignity,
                "lord_shadbala": lord_shadbala,
                "occupants": occupants,
                "aspecting_planets": aspecting_planets,
                "benefic_influences_count": len(benefic_influences),
                "malefic_influences_count": len(malefic_influences),
                "house_score": final_score,
                "strength_rating": "Strong" if final_score >= 70 else ("Moderate" if final_score >= 45 else "Afflicted"),
                # ── New v2.0 fields ──
                "net_benefic_score": round(net_benefic_score, 2),
                "net_malefic_score": round(net_malefic_score, 2),
                "net_influence_score": net_influence_score,
                "is_afflicted": is_afflicted,
                "is_protected": is_protected,
                "strongest_influence": strongest_influence,
                "weakest_influence": weakest_influence,
                "benefic_occupants_count": len(benefic_occupants),
                "malefic_occupants_count": len(malefic_occupants),
                "benefic_aspecting_count": len(benefic_aspecting),
                "malefic_aspecting_count": len(malefic_aspecting),
                "effective_aspecting_planets": effective_aspecting,
                "house_type": house_type,
                "is_kendra": h in HouseAnalysisEngine.KENDRA_HOUSES,
                "is_trikona": h in HouseAnalysisEngine.TRIKONA_HOUSES,
                "is_trik": h in HouseAnalysisEngine.TRIK_HOUSES,
                "is_upachaya": h in HouseAnalysisEngine.UPACHAYA_HOUSES
            }

        return houses_analysis
