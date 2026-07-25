# -*- coding: utf-8 -*-
"""
Functional Planet Classification Engine.
Determines Functional Benefics, Functional Malefics, Yogakaraka, Maraka, Badhakesh,
and Trik/Kendra/Trikona lords according to BPHS classical rules for all 12 Ascendants.
"""

class FunctionalPlanetEngine:
    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']

    # Classical BPHS Functional Benefics and Malefics by Ascendant Index (0..11)
    FUNCTIONAL_MAP = {
        0: { "fb": ["Sun", "Mars", "Jupiter"], "fm": ["Mercury", "Venus", "Saturn"], "yk": "Mars" },        # Aries
        1: { "fb": ["Sun", "Mercury", "Saturn"], "fm": ["Moon", "Mars", "Jupiter"], "yk": "Saturn" },     # Taurus
        2: { "fb": ["Venus", "Saturn"], "fm": ["Sun", "Mars", "Jupiter"], "yk": None },                  # Gemini
        3: { "fb": ["Mars", "Jupiter"], "fm": ["Mercury", "Venus", "Saturn"], "yk": "Mars" },             # Cancer
        4: { "fb": ["Sun", "Mars", "Jupiter"], "fm": ["Mercury", "Venus", "Saturn"], "yk": "Mars" },        # Leo
        5: { "fb": ["Venus", "Saturn"], "fm": ["Moon", "Mars", "Jupiter"], "yk": None },                  # Virgo
        6: { "fb": ["Saturn", "Mercury"], "fm": ["Sun", "Mars", "Jupiter"], "yk": "Saturn" },             # Libra
        7: { "fb": ["Sun", "Moon", "Jupiter"], "fm": ["Mercury", "Venus", "Saturn"], "yk": "Jupiter" },   # Scorpio
        8: { "fb": ["Sun", "Mars"], "fm": ["Mercury", "Venus", "Saturn"], "yk": None },                   # Sagittarius
        9: { "fb": ["Venus", "Mercury", "Saturn"], "fm": ["Sun", "Moon", "Mars"], "yk": "Venus" },        # Capricorn
        10: { "fb": ["Venus", "Saturn"], "fm": ["Sun", "Moon", "Jupiter"], "yk": "Venus" },               # Aquarius
        11: { "fb": ["Mars", "Moon"], "fm": ["Sun", "Mercury", "Venus", "Saturn"], "yk": None }           # Pisces
    }

    @staticmethod
    def classify_planets(ascendant_sign_idx: int) -> dict:
        asc_name = FunctionalPlanetEngine.SIGN_NAMES[ascendant_sign_idx % 12]
        
        # 1. House Lords (1 to 12)
        house_lords = {}
        for h in range(1, 13):
            s_idx = (ascendant_sign_idx + h - 1) % 12
            house_lords[h] = FunctionalPlanetEngine.SIGN_LORDS[s_idx]

        # 2. Functional Benefics & Malefics
        rule_data = FunctionalPlanetEngine.FUNCTIONAL_MAP.get(ascendant_sign_idx % 12, {
            "fb": ["Sun", "Mars", "Jupiter"], "fm": ["Mercury", "Venus", "Saturn"], "yk": None
        })

        # 3. Maraka Lords (2nd & 7th House Lords)
        marakas = list(set([house_lords[2], house_lords[7]]))

        # 4. Badhakesh Lord
        # Movable (Aries, Cancer, Libra, Cap) -> 9th House
        # Fixed (Taurus, Leo, Scorpio, Aqu) -> 7th House
        # Dual (Gemini, Virgo, Sag, Pisces) -> 11th House
        movable = [0, 3, 6, 9]
        fixed = [1, 4, 7, 10]
        if (ascendant_sign_idx % 12) in movable:
            badhakesh = house_lords[9]
        elif (ascendant_sign_idx % 12) in fixed:
            badhakesh = house_lords[7]
        else:
            badhakesh = house_lords[11]

        # 5. Trik, Kendra, Trikona Lords
        trik_lords = list(set([house_lords[6], house_lords[8], house_lords[12]]))
        kendra_lords = list(set([house_lords[1], house_lords[4], house_lords[7], house_lords[10]]))
        trikona_lords = list(set([house_lords[1], house_lords[5], house_lords[9]]))

        return {
            "ascendant_sign": asc_name,
            "ascendant_index": ascendant_sign_idx % 12,
            "functional_benefics": rule_data["fb"],
            "functional_malefics": rule_data["fm"],
            "yogakaraka": rule_data["yk"],
            "marakas": marakas,
            "badhakesh": badhakesh,
            "trik_lords": trik_lords,
            "kendra_lords": kendra_lords,
            "trikona_lords": trikona_lords
        }
