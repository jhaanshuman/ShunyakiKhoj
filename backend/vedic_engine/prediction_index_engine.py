# -*- coding: utf-8 -*-
"""
Prediction Index Engine v2.0.
Generates an AI-friendly executive index with 25+ fields covering strongest/weakest planets,
best/most afflicted houses, dominant elements/gunas/tattvas, life theme scores, and top yogas/rules.
"""

class PredictionIndexEngine:
    # Element mapping for signs (0-11)
    ELEMENT_MAP = {
        0: 'Fire', 1: 'Earth', 2: 'Air', 3: 'Water',
        4: 'Fire', 5: 'Earth', 6: 'Air', 7: 'Water',
        8: 'Fire', 9: 'Earth', 10: 'Air', 11: 'Water'
    }
    # Guna mapping for signs
    GUNA_MAP = {
        0: 'Rajas', 1: 'Tamas', 2: 'Rajas', 3: 'Tamas',
        4: 'Rajas', 5: 'Tamas', 6: 'Rajas', 7: 'Tamas',
        8: 'Sattva', 9: 'Tamas', 10: 'Sattva', 11: 'Sattva'
    }
    # Tattva (element) — more specific
    TATTVA_MAP = {
        0: 'Agni', 1: 'Prithvi', 2: 'Vayu', 3: 'Jala',
        4: 'Agni', 5: 'Prithvi', 6: 'Vayu', 7: 'Jala',
        8: 'Agni', 9: 'Prithvi', 10: 'Vayu', 11: 'Jala'
    }

    KENDRA_HOUSES = [1, 4, 7, 10]
    TRIKONA_HOUSES = [1, 5, 9]

    LIFE_THEME_MAP = {
        'career': 'Career & Authority',
        'marriage': 'Relationships & Partnership',
        'wealth': 'Finance & Prosperity',
        'health': 'Vitality & Wellbeing',
        'spirituality': 'Spiritual Growth & Wisdom',
        'education': 'Education & Intellect',
        'property': 'Property & Assets',
        'children': 'Children & Legacy',
        'foreign': 'Foreign Lands & Travel',
        'litigation': 'Conflicts & Litigation',
        'business': 'Business & Trade',
        'government': 'Government & Authority',
        'fame': 'Fame & Recognition',
        'longevity': 'Longevity & Endurance',
        'siblings': 'Siblings & Courage',
        'parents': 'Parents & Lineage'
    }

    @staticmethod
    def generate_prediction_index(master_obj: dict) -> dict:
        rankings = master_obj.get('planet_ranking', [])
        houses_analysis = master_obj.get('house_analysis', {})
        indicators = master_obj.get('event_indicators', {})
        planets_data = master_obj.get('planets', {})
        advanced_yogas = master_obj.get('advanced_yogas', [])
        rule_matches = master_obj.get('rule_matches', [])
        yogas = master_obj.get('yogas', [])

        strongest_planet = rankings[0]['name'] if rankings else 'Jupiter'
        weakest_planet = rankings[-1]['name'] if rankings else 'Moon'

        # Find best and most afflicted houses
        sorted_houses = sorted(
            houses_analysis.values(),
            key=lambda h: h.get('house_score', 50.0),
            reverse=True
        )
        best_house = sorted_houses[0].get('house_number', 1) if sorted_houses else 10
        most_afflicted_house = sorted_houses[-1].get('house_number', 8) if sorted_houses else 8

        # Dominant element/guna/tattva (from planet sign positions weighted by strength)
        element_scores = {}
        guna_scores = {}
        tattva_scores = {}
        for rank_entry in rankings:
            p_name = rank_entry.get('name')
            p_score = rank_entry.get('score', 50)
            p_data = planets_data.get(p_name, {})
            s_idx = p_data.get('sign_index', 0)
            elem = PredictionIndexEngine.ELEMENT_MAP.get(s_idx, 'Fire')
            guna = PredictionIndexEngine.GUNA_MAP.get(s_idx, 'Rajas')
            tattva = PredictionIndexEngine.TATTVA_MAP.get(s_idx, 'Agni')
            element_scores[elem] = element_scores.get(elem, 0) + p_score
            guna_scores[guna] = guna_scores.get(guna, 0) + p_score
            tattva_scores[tattva] = tattva_scores.get(tattva, 0) + p_score

        dominant_element = max(element_scores, key=element_scores.get) if element_scores else 'Fire'
        dominant_guna = max(guna_scores, key=guna_scores.get) if guna_scores else 'Rajas'
        dominant_tattva = max(tattva_scores, key=tattva_scores.get) if tattva_scores else 'Agni'

        # Dominant house (highest score among all)
        dominant_house = sorted_houses[0].get('house_number', 1) if sorted_houses else 1

        # Dominant trikona and kendra
        trikona_houses = {h: houses_analysis.get(f'house_{h}', {}).get('house_score', 50) for h in PredictionIndexEngine.TRIKONA_HOUSES}
        dominant_trikona = max(trikona_houses, key=trikona_houses.get) if trikona_houses else 1
        kendra_houses = {h: houses_analysis.get(f'house_{h}', {}).get('house_score', 50) for h in PredictionIndexEngine.KENDRA_HOUSES}
        dominant_kendra = max(kendra_houses, key=kendra_houses.get) if kendra_houses else 1

        # Top yogas
        all_yogas = list(yogas) + list(advanced_yogas)
        sorted_yogas = sorted(all_yogas, key=lambda y: y.get('confidence', y.get('strength', 0)), reverse=True)
        top_3_yogas = [{'name': y.get('name', ''), 'confidence': y.get('confidence', 0)} for y in sorted_yogas[:3]]
        strongest_yoga = sorted_yogas[0].get('name', '') if sorted_yogas else ''

        # Strongest dosha (affliction)
        dosha_markers = []
        for y in all_yogas:
            name = y.get('name', '')
            if 'Dosha' in name or 'Kalasarpa' in name or 'Mangal' in name or 'Kemadruma' in name:
                dosha_markers.append(name)
        strongest_dosha = dosha_markers[0] if dosha_markers else 'None detected'

        # Top rules
        sorted_rules = sorted(rule_matches, key=lambda r: r.get('confidence', 0), reverse=True)
        top_3_rules = [{'id': r.get('id', ''), 'title': r.get('title', ''), 'domain': r.get('domain', ''), 'confidence': r.get('confidence', 0)} for r in sorted_rules[:3]]

        # Life theme scores
        life_theme_scores = {
            domain: round(indicators.get(domain, 50.0), 1)
            for domain in PredictionIndexEngine.LIFE_THEME_MAP
        }

        # Strongest and weakest life areas
        if life_theme_scores:
            strongest_life_theme_key = max(life_theme_scores, key=life_theme_scores.get)
            weakest_life_area_key = min(life_theme_scores, key=life_theme_scores.get)
            strongest_life_theme = PredictionIndexEngine.LIFE_THEME_MAP.get(strongest_life_theme_key, strongest_life_theme_key)
            weakest_life_area = PredictionIndexEngine.LIFE_THEME_MAP.get(weakest_life_area_key, weakest_life_area_key)
        else:
            strongest_life_theme = 'Career & Authority'
            weakest_life_area = 'Foreign Lands & Travel'

        return {
            # ── Backward-compatible fields ──
            "strongest_planet": strongest_planet,
            "weakest_planet": weakest_planet,
            "best_house": best_house,
            "most_afflicted_house": most_afflicted_house,
            "career_score": indicators.get('career', 50.0),
            "marriage_score": indicators.get('marriage', 50.0),
            "wealth_score": indicators.get('wealth', 50.0),
            "health_score": indicators.get('health', 50.0),
            "spiritual_score": indicators.get('spirituality', 50.0),
            # ── New v2.0 fields ──
            "strongest_yoga": strongest_yoga,
            "strongest_dosha": strongest_dosha,
            "dominant_element": dominant_element,
            "dominant_guna": dominant_guna,
            "dominant_tattva": dominant_tattva,
            "dominant_house": dominant_house,
            "dominant_trikona": dominant_trikona,
            "dominant_kendra": dominant_kendra,
            "strongest_life_theme": strongest_life_theme,
            "weakest_life_area": weakest_life_area,
            "top_3_yogas": top_3_yogas,
            "top_3_rules": top_3_rules,
            "life_theme_scores": life_theme_scores,
            "planet_scores_summary": [
                {"planet": r.get('name'), "score": r.get('score')}
                for r in rankings[:5]
            ]
        }
