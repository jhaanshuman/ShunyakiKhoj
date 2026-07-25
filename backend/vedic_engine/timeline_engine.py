# -*- coding: utf-8 -*-
"""
Timeline Engine v1.0.
Builds a multi-layer timeline of significant astrological periods.
Includes: Vimshottari dasha, current transits, upcoming planetary returns.
Each timeline entry includes both absolute years AND life-age.
"""

from datetime import datetime, timedelta

class TimelineEngine:
    DASHA_LORDS_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    DASHA_YEARS = {'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17}
    TOTAL_DASHA_YEARS = 120

    PLANET_SIGNIFICANCE = {
        'Sun': ['Career', 'Government', 'Father', 'Fame', 'Health'],
        'Moon': ['Mind', 'Mother', 'Property', 'Wealth', 'Emotions'],
        'Mars': ['Property', 'Siblings', 'Career', 'Accidents', 'Courage'],
        'Mercury': ['Education', 'Business', 'Communication', 'Trade'],
        'Jupiter': ['Wealth', 'Children', 'Wisdom', 'Spirituality', 'Marriage'],
        'Venus': ['Marriage', 'Luxury', 'Arts', 'Wealth', 'Vehicles'],
        'Saturn': ['Career', 'Discipline', 'Longevity', 'Service', 'Delays'],
        'Rahu': ['Foreign Travel', 'Technology', 'Ambition', 'Unexpected Fame'],
        'Ketu': ['Spirituality', 'Liberation', 'Occult', 'Detachment']
    }

    @staticmethod
    def build(master_obj: dict) -> dict:
        dasha = master_obj.get('dasha', {})
        birth_data = master_obj.get('birth_data', {})
        transits = master_obj.get('transits', {})
        planet_state = master_obj.get('planet_state', {})

        birth_date_str = birth_data.get('birth_date', None)
        birth_time_str = birth_data.get('birth_time', '12:00')

        # Parse birth date
        birth_dt = None
        if birth_date_str:
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                try:
                    birth_dt = datetime.strptime(str(birth_date_str), fmt)
                    break
                except:
                    pass

        today = datetime.utcnow().replace(tzinfo=None)
        current_age = 0
        if birth_dt:
            current_age = (today - birth_dt).days // 365

        # Build dasha timeline from vimshottari data
        vimshottari = dasha.get('vimshottari', [])
        dasha_timeline = []

        for md in vimshottari:
            lord = md.get('lord', '')
            start = md.get('start_date', '')
            end = md.get('end_date', '')
            
            # Parse dates
            start_dt = None; end_dt = None
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y']:
                try:
                    start_dt = datetime.strptime(str(start)[:10], '%Y-%m-%d'); break
                except:
                    pass
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y']:
                try:
                    end_dt = datetime.strptime(str(end)[:10], '%Y-%m-%d'); break
                except:
                    pass

            age_start = ((start_dt - birth_dt).days // 365) if (start_dt and birth_dt) else None
            age_end = ((end_dt - birth_dt).days // 365) if (end_dt and birth_dt) else None

            is_current = start_dt and end_dt and start_dt <= today <= end_dt if start_dt and end_dt else False
            is_upcoming = start_dt and start_dt > today if start_dt else False
            is_past = end_dt and end_dt < today if end_dt else False

            p_state = planet_state.get(lord, {})
            lord_strength = p_state.get('overall_strength', 50.0)
            dignity = p_state.get('dignity_state', 'Neutral')

            significance = TimelineEngine.PLANET_SIGNIFICANCE.get(lord, [])
            period_quality = 'Favorable' if lord_strength >= 60 else ('Challenging' if lord_strength < 40 else 'Mixed')

            # Antardashas
            antardashas = md.get('antardashas', [])
            ad_timeline = []
            for ad in antardashas:
                ad_lord = ad.get('lord', '')
                ad_start = ad.get('start_date', '')
                ad_end = ad.get('end_date', '')
                ad_start_dt = None
                try:
                    ad_start_dt = datetime.strptime(str(ad_start)[:10], '%Y-%m-%d')
                except:
                    pass
                ad_is_current = False
                if ad_start_dt:
                    try:
                        ad_end_dt = datetime.strptime(str(ad_end)[:10], '%Y-%m-%d')
                        ad_is_current = ad_start_dt <= today <= ad_end_dt
                    except:
                        pass

                ad_state = planet_state.get(ad_lord, {})
                ad_lord_strength = ad_state.get('overall_strength', 50.0)

                ad_start_year = ad_start_dt.year if ad_start_dt else None
                ad_end_year = None
                try:
                    _ad_end_dt = datetime.strptime(str(ad_end)[:10], '%Y-%m-%d')
                    ad_end_year = _ad_end_dt.year
                except:
                    pass

                ad_timeline.append({
                    "lord": ad_lord,
                    # Absolute years (primary)
                    "start_year": ad_start_year,
                    "end_year": ad_end_year,
                    # ISO dates (supplementary)
                    "start_date": ad_start,
                    "end_date": ad_end,
                    "is_current": ad_is_current,
                    "lord_strength": ad_lord_strength,
                    "significance": TimelineEngine.PLANET_SIGNIFICANCE.get(ad_lord, []),
                    "period_quality": 'Favorable' if ad_lord_strength >= 60 else ('Challenging' if ad_lord_strength < 40 else 'Mixed')
                })

            start_year = start_dt.year if start_dt else None
            end_year = end_dt.year if end_dt else None
            duration_years = round((end_dt - start_dt).days / 365.25, 1) if (start_dt and end_dt) else None

            dasha_timeline.append({
                "type": "Mahadasha",
                "lord": lord,
                # Absolute years (primary — Q2 preference)
                "start_year": start_year,
                "end_year": end_year,
                "duration_years": duration_years,
                # ISO dates (supplementary)
                "start_date": start,
                "end_date": end,
                # Age at start/end (supplementary)
                "age_start": age_start,
                "age_end": age_end,
                "is_current": is_current,
                "is_upcoming": is_upcoming,
                "is_past": is_past,
                "lord_strength": round(lord_strength, 1),
                "dignity": dignity,
                "period_quality": period_quality,
                "life_domains": significance,
                "antardashas": ad_timeline
            })

        # Current transit highlights
        transit_highlights = []
        transit_planets = transits.get('planets', {})
        for p, t_data in transit_planets.items():
            house = t_data.get('house', 0)
            if house in [1, 4, 5, 7, 9, 10]:
                transit_highlights.append({
                    "planet": p,
                    "transit_house": house,
                    "transit_sign": t_data.get('sign', ''),
                    "significance": TimelineEngine.PLANET_SIGNIFICANCE.get(p, [])
                })

        return {
            "current_age": current_age,
            "birth_date": birth_date_str,
            "current_date": today.strftime('%Y-%m-%d'),
            "dasha_timeline": dasha_timeline,
            "transit_highlights": transit_highlights,
            "engine_version": "TimelineEngine v1.0"
        }
