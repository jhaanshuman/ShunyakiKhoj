# -*- coding: utf-8 -*-
"""
AI Context Engine v1.0.
Builds a comprehensive, structured context object for AI/LLM consumption.
Replaces the old ai_graph with a richer ai_context that includes:
- All prediction domains with evidence
- Current dasha interpretation
- Yoga narratives
- House lord themes
- Planet functional roles
- Recommended areas of focus
"""

class AIContextEngine:

    HOUSE_THEMES = {
        1: 'physical vitality and self-image',
        2: 'family wealth and speech',
        3: 'courage, communication, and siblings',
        4: 'home, mother, property, and emotional security',
        5: 'intelligence, creativity, children, and investments',
        6: 'health challenges, enemies, and service',
        7: 'marriage, partnerships, and trade',
        8: 'longevity, transformation, and hidden matters',
        9: 'fortune, father, dharma, and higher knowledge',
        10: 'career, reputation, and public authority',
        11: 'income, gains, and social networks',
        12: 'foreign lands, spiritual liberation, and losses'
    }

    DIGNITY_INTERPRETATION = {
        'Exalted': 'maximum strength and full positive expression',
        'Moolatrikona': 'near-maximum strength in primary domain',
        'Swakshetra (Own Sign)': 'comfortable and natural expression',
        'Great Friend (Adhi Mitra)': 'cooperative and supportive energy',
        'Friend (Mitra)': 'generally positive expression',
        'Neutral (Sama)': 'neutral expression; dependent on aspects',
        'Enemy (Shatru)': 'strained expression; needs remediation',
        'Great Enemy (Adhi Shatru)': 'severely strained; significant remediation needed',
        'Debilitated': 'weakest expression; potential Neecha Bhanga if cancelled'
    }

    DASHA_INTERPRETATION = {
        'Sun': 'period of career advancement, father\'s health, government connections, authority',
        'Moon': 'period of emotional shifts, property matters, mother, public reputation changes',
        'Mars': 'period of action, property, siblings, accidents, and courage-driven initiatives',
        'Mercury': 'period of business, education, communication, trade, and intellectual growth',
        'Jupiter': 'period of wisdom, wealth growth, children, marriage blessings, spirituality',
        'Venus': 'period of luxury, beauty, relationships, arts, marriage, and material enjoyment',
        'Saturn': 'period of hard work, discipline, delays, property, and long-term rewards',
        'Rahu': 'period of rapid change, foreign contacts, ambition, unusual opportunities',
        'Ketu': 'period of spiritual turning point, detachment, occult interests, health vigilance'
    }

    @staticmethod
    def generate(master_obj: dict) -> dict:
        dignities = master_obj.get('dignity', {})
        house_analysis = master_obj.get('house_analysis', {})
        planet_state = master_obj.get('planet_state', {})
        functional = master_obj.get('functional_classification', {})
        domain_synthesis = master_obj.get('domain_synthesis', [])
        rule_matches = master_obj.get('rule_matches', [])
        advanced_yogas = master_obj.get('advanced_yogas', [])
        yogas = master_obj.get('yogas', [])
        planet_network = master_obj.get('planet_influence_network', [])
        timeline = master_obj.get('timeline', {})
        dasha = master_obj.get('dasha', {})
        houses = master_obj.get('houses', {})
        planets = master_obj.get('planets', {})
        prediction_index = master_obj.get('prediction_index', {})
        shadbala = master_obj.get('shadbala', {})

        asc_lon = houses.get('ascendant_sidereal_lon', 0.0)
        asc_sign_idx = int(asc_lon / 30.0) % 12
        SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']

        lagna_sign = SIGN_NAMES[asc_sign_idx]
        lagna_lord = SIGN_LORDS[asc_sign_idx]

        # Current dasha
        vimshottari = dasha.get('vimshottari', [])
        current_md = vimshottari[0] if vimshottari else {}
        md_lord = current_md.get('lord', '')
        antardashas = current_md.get('antardashas', [])
        current_ad = antardashas[0] if antardashas else {}
        ad_lord = current_ad.get('lord', '')
        prd_lord = current_ad.get('pratyantardashas', [{}])[0].get('lord', '') if current_ad.get('pratyantardashas') else ''

        # Planet context (brief per planet)
        planet_context = []
        for node in planet_network:
            p = node['planet']
            p_state = planet_state.get(p, {})
            strength_label = p_state.get('effective_strength_label', 'Moderate')
            dig_state = p_state.get('dignity_state', 'Neutral')
            dig_interp = AIContextEngine.DIGNITY_INTERPRETATION.get(dig_state, 'neutral expression')
            planet_context.append({
                "planet": p,
                "house": node['house'],
                "dignity": dig_state,
                "strength": strength_label,
                "interpretation": dig_interp,
                "life_areas": node.get('life_areas_influenced', []),
                "functional_role": node.get('functional_role', 'Neutral')
            })

        # Top 5 domain predictions
        top_predictions = []
        for ds in sorted(domain_synthesis, key=lambda x: x.get('domain_score', 0), reverse=True)[:5]:
            top_predictions.append({
                "domain": ds.get('domain_display', ''),
                "score": ds.get('domain_score', 0),
                "summary": ds.get('summary', ''),
                "rule_count": ds.get('rule_count', 0),
                "yoga_count": ds.get('yoga_count', 0),
                "conflicting_factors": ds.get('conflicting_factors', [])[:3]
            })

        # Top active yogas (by confidence)
        all_yogas = list(yogas) + list(advanced_yogas)
        top_yogas = sorted(all_yogas, key=lambda y: y.get('confidence', 0), reverse=True)[:10]
        yoga_narratives = [
            {"name": y.get('name', ''), "category": y.get('category', ''), "description": y.get('description', '')}
            for y in top_yogas
        ]

        # House lord themes
        house_themes = []
        for h in range(1, 13):
            sign_idx = (asc_sign_idx + h - 1) % 12
            lord = SIGN_LORDS[sign_idx]
            p_state = planet_state.get(lord, {})
            ha = house_analysis.get(f'house_{h}', {})
            house_themes.append({
                "house": h,
                "theme": AIContextEngine.HOUSE_THEMES.get(h, ''),
                "lord": lord,
                "lord_strength": p_state.get('effective_strength_label', 'Moderate'),
                "house_score": ha.get('house_score', 50.0),
                "is_afflicted": ha.get('is_afflicted', False),
                "is_protected": ha.get('is_protected', False)
            })

        # Yogakaraka
        yogakaraka = functional.get('yogakaraka', None)
        yogakaraka_context = {}
        if yogakaraka:
            yk_state = planet_state.get(yogakaraka, {})
            yogakaraka_context = {
                "planet": yogakaraka,
                "strength": yk_state.get('effective_strength_label', 'Moderate'),
                "house": yk_state.get('house', 0),
                "dignity": yk_state.get('dignity_state', 'Neutral'),
                "message": f"{yogakaraka} is the most powerful planet for {lagna_sign} Lagna, ruling both a Kendra and a Trikona."
            }

        # Current dasha context
        current_dasha_context = {
            "mahadasha_lord": md_lord,
            "antardasha_lord": ad_lord,
            "pratyantardasha_lord": prd_lord,
            "md_start": current_md.get('start_date', ''),
            "md_end": current_md.get('end_date', ''),
            "interpretation": AIContextEngine.DASHA_INTERPRETATION.get(md_lord, ''),
            "md_lord_strength": planet_state.get(md_lord, {}).get('effective_strength_label', 'Moderate'),
            "ad_lord_strength": planet_state.get(ad_lord, {}).get('effective_strength_label', 'Moderate'),
        }

        # Key focus areas (top 3 domains)
        focus_areas = [d['domain_display'] for d in domain_synthesis[:3]] if domain_synthesis else []

        # Lagna and chart summary
        chart_summary = {
            "lagna_sign": lagna_sign,
            "lagna_lord": lagna_lord,
            "lagna_lord_house": planet_state.get(lagna_lord, {}).get('house', 0),
            "lagna_lord_strength": planet_state.get(lagna_lord, {}).get('effective_strength_label', 'Moderate'),
            "moon_sign": SIGN_NAMES[planets.get('Moon', {}).get('sign_index', 0)] if 'Moon' in planets else '',
            "sun_sign": SIGN_NAMES[planets.get('Sun', {}).get('sign_index', 0)] if 'Sun' in planets else '',
            "total_active_yogas": len(all_yogas),
            "total_active_rules": len(rule_matches),
            "overall_chart_strength": prediction_index.get('overall_chart_strength', 50.0),
            "primary_life_theme": prediction_index.get('primary_life_theme', 'Balanced')
        }

        return {
            "version": "AIContextEngine v1.0",
            "chart_summary": chart_summary,
            "yogakaraka": yogakaraka_context,
            "current_dasha": current_dasha_context,
            "top_predictions": top_predictions,
            "yoga_narratives": yoga_narratives,
            "house_themes": house_themes,
            "planet_context": planet_context,
            "recommended_focus_areas": focus_areas,
            "total_yogas_detected": len(all_yogas),
            "total_rules_matched": len(rule_matches)
        }
