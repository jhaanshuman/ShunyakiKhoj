# -*- coding: utf-8 -*-
"""
Planetary Aspect Engine (Graha & Rashi Drishti) v2.0.
Calculates both classical Graha Drishti (with orbs, applying/separating status,
and aspect strength) and Jaimini Rashi Drishti.
New: 6-tier orb classification, is_effective filter, is_valid flag.
"""

class AspectEngine:
    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    # 6-tier orb classification
    ORB_CLASSES = [
        (1.0,  'Exact',    True,  True),
        (3.0,  'Tight',    True,  True),
        (6.0,  'Close',    True,  True),
        (9.0,  'Moderate', True,  True),
        (12.0, 'Wide',     False, True),
        (360.0,'Outside',  False, False),
    ]

    @staticmethod
    def classify_orb(orb: float):
        """Returns (orb_class, is_effective, is_valid, effective_strength)"""
        for limit, label, effective, valid in AspectEngine.ORB_CLASSES:
            if orb < limit:
                # Calculate strength: linear scale within the tier
                if not valid:
                    return label, False, False, 0.0, f"Outside effective orb ({orb:.2f}°)"
                if not effective:
                    # Wide tier: strength 1-15%
                    strength = max(1.0, round((1.0 - (orb / 12.0)) * 100.0, 2))
                    return label, False, True, strength, f"Wide orb — present but not effective"
                # Effective tiers: strength 40-100%
                if label == 'Exact':
                    strength = round(90.0 + (1.0 - orb) * 10.0, 2)
                elif label == 'Tight':
                    strength = round(70.0 + ((3.0 - orb) / 2.0) * 20.0, 2)
                elif label == 'Close':
                    strength = round(40.0 + ((6.0 - orb) / 3.0) * 30.0, 2)
                elif label == 'Moderate':
                    strength = round(15.0 + ((9.0 - orb) / 3.0) * 25.0, 2)
                else:
                    strength = round(max(0.0, (1.0 - (orb / 12.0)) * 100.0), 2)
                strength = min(100.0, max(0.0, strength))
                return label, True, True, strength, f"{label} orb ({orb:.2f}°) — effective aspect"
        return 'Outside', False, False, 0.0, f"Outside effective orb ({orb:.2f}°)"

    @staticmethod
    def calculate_aspects(planets_data: dict, ascendant_sign_idx: int) -> dict:
        graha_aspects = []
        rashi_aspects = []

        planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        
        special_aspects = {
            'Mars': [4, 7, 8],
            'Jupiter': [5, 7, 9],
            'Saturn': [3, 7, 10],
            'Rahu': [5, 7, 9],
            'Ketu': [5, 7, 9],
            'Sun': [7],
            'Moon': [7],
            'Mercury': [7],
            'Venus': [7]
        }

        for p1 in planet_names:
            if p1 not in planets_data:
                continue
            d1 = planets_data[p1]
            lon1 = d1.get('sidereal_lon', 0.0)
            sign1_idx = d1.get('sign_index', 0)
            speed1 = d1.get('speed', 1.0)
            
            allowed_house_aspects = special_aspects.get(p1, [7])
            
            for house_offset in allowed_house_aspects:
                target_sign_idx = (sign1_idx + house_offset - 1) % 12
                target_house_num = ((target_sign_idx - ascendant_sign_idx + 12) % 12) + 1
                
                for p2 in planet_names:
                    if p1 == p2 or p2 not in planets_data:
                        continue
                    d2 = planets_data[p2]
                    sign2_idx = d2.get('sign_index', 0)
                    
                    if sign2_idx == target_sign_idx:
                        lon2 = d2.get('sidereal_lon', 0.0)
                        speed2 = d2.get('speed', 1.0)
                        
                        diff = (lon2 - lon1 + 360.0) % 360.0
                        expected_angle = (house_offset - 1) * 30.0
                        if house_offset == 7:
                            expected_angle = 180.0
                        
                        orb = abs(diff - expected_angle)
                        if orb > 180.0:
                            orb = 360.0 - orb
                            
                        rel_speed = speed1 - speed2
                        applying = (diff < expected_angle and rel_speed > 0) or (diff > expected_angle and rel_speed < 0)
                        
                        # Legacy strength (backward compat)
                        max_orb = 12.0
                        strength_pct = max(0.0, round((1.0 - (orb / max_orb)) * 100.0, 2))
                        
                        # New: 6-tier classification
                        orb_class, is_effective, is_valid, effective_strength, reason = AspectEngine.classify_orb(orb)
                        
                        graha_aspects.append({
                            # ── Backward-compatible fields ──
                            "aspecting_planet": p1,
                            "target_planet": p2,
                            "aspect_house": house_offset,
                            "target_house": target_house_num,
                            "target_sign": AspectEngine.SIGN_NAMES[target_sign_idx],
                            "orb": round(orb, 4),
                            "exact_aspect": orb < 1.0,
                            "is_applying": applying,
                            "strength_percentage": strength_pct,
                            # ── New v2.0 fields ──
                            "orb_class": orb_class,
                            "is_effective": is_effective,
                            "is_valid": is_valid,
                            "effective_strength": effective_strength,
                            "reason": reason
                        })

        # RASHI DRISHTI (unchanged)
        movable = [0, 3, 6, 9]
        fixed = [1, 4, 7, 10]
        dual = [2, 5, 8, 11]

        for s1 in range(12):
            target_signs = []
            if s1 in movable:
                for s2 in fixed:
                    if s2 != (s1 + 1) % 12 and s2 != (s1 - 1 + 12) % 12:
                        target_signs.append(s2)
            elif s1 in fixed:
                for s2 in movable:
                    if s2 != (s1 + 1) % 12 and s2 != (s1 - 1 + 12) % 12:
                        target_signs.append(s2)
            elif s1 in dual:
                for s2 in dual:
                    if s2 != s1:
                        target_signs.append(s2)

            s1_planets = [p for p in planet_names if p in planets_data and planets_data[p].get('sign_index') == s1]
            if s1_planets:
                for t_sign in target_signs:
                    t_planets = [p for p in planet_names if p in planets_data and planets_data[p].get('sign_index') == t_sign]
                    rashi_aspects.append({
                        "aspecting_sign": AspectEngine.SIGN_NAMES[s1],
                        "target_sign": AspectEngine.SIGN_NAMES[t_sign],
                        "aspecting_planets": s1_planets,
                        "target_planets": t_planets
                    })

        return {
            "planetary_aspects": graha_aspects,
            "rashi_aspects": rashi_aspects
        }
