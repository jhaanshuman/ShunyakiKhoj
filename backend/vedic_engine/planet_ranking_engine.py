# -*- coding: utf-8 -*-
"""
Planet Strength Ranking Engine.
Synthesizes Shadbala, Vimsopaka, Dignity state, Aspect support, Combustion, and Retrogression
into a normalized composite strength score (0-100) and ranks planets from 1 to 9.
"""

class PlanetRankingEngine:
    PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

    @staticmethod
    def rank_planets(master_obj: dict) -> list:
        planets_data = master_obj.get('planets', {})
        dignities = master_obj.get('dignity', {})
        shadbala = master_obj.get('shadbala', {})
        aspects = master_obj.get('planetary_aspects', [])
        
        ranking_list = []

        for p in PlanetRankingEngine.PLANETS:
            if p not in planets_data:
                continue
            d_info = planets_data[p]
            dignity_info = dignities.get(p, {})
            dig_state = dignity_info.get('dignity_state', 'Neutral')
            shad_val = shadbala.get(p, 350.0)

            # 1. Base Score from Shadbala (Normal benchmark = 360 Virupas)
            base_score = min(40.0, (shad_val / 600.0) * 40.0)

            # 2. Dignity Contribution (Max 30 pts)
            dig_pts = 15.0
            if "Exalted" in dig_state or "Moolatrikona" in dig_state:
                dig_pts = 30.0
            elif "Own Sign" in dig_state or "Great Friend" in dig_state:
                dig_pts = 24.0
            elif "Friend" in dig_state:
                dig_pts = 20.0
            elif "Enemy" in dig_state:
                dig_pts = 10.0
            elif "Debilitated" in dig_state or "Great Enemy" in dig_state:
                dig_pts = 4.0

            # 3. Retrogression Boost (+10 pts for natural malefics/benefics in good sign)
            retro_pts = 10.0 if d_info.get('is_retrograde', False) else 0.0

            # 4. Combustion Penalty (-15 pts if severe combustion)
            combust_penalty = 15.0 if d_info.get('is_combust', False) else 0.0

            # 5. Aspect Support (Aspects received from benefics/malefics)
            aspect_pts = 0.0
            for asp in aspects:
                if asp.get('target_planet') == p:
                    asp_p = asp.get('aspecting_planet')
                    if asp_p in ['Jupiter', 'Venus', 'Mercury']:
                        aspect_pts += 5.0
                    elif asp_p in ['Saturn', 'Mars', 'Rahu']:
                        aspect_pts -= 4.0

            total_score = base_score + dig_pts + retro_pts - combust_penalty + aspect_pts
            final_score = min(100.0, max(5.0, round(total_score, 2)))

            ranking_list.append({
                "name": p,
                "score": final_score,
                "dignity": dig_state,
                "shadbala_virupas": round(shad_val, 2),
                "is_retrograde": d_info.get('is_retrograde', False),
                "is_combust": d_info.get('is_combust', False),
                "sign": d_info.get('sign_name', 'Aries'),
                "house": d_info.get('house', 1)
            })

        # Sort descending by score
        ranking_list.sort(key=lambda x: x['score'], reverse=True)
        
        # Add rank index
        for idx, item in enumerate(ranking_list, start=1):
            item['rank'] = idx

        return ranking_list
