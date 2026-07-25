# -*- coding: utf-8 -*-
"""
Planet Engine: Ephemeris Calculations for Planets, Nakshatras, Dignities, and Aspects.
"""
from dataclasses import dataclass, field
import math
from typing import Dict, List, Any, Optional, Tuple

try:
    import swisseph as swe
    HAS_SWISSEPH = True
except ImportError:
    try:
        import pyswisseph as swe
        HAS_SWISSEPH = True
    except ImportError:
        swe = None
        HAS_SWISSEPH = False


SIGN_NAMES = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira',
    'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
    'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati',
    'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
    'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
    'Uttara Bhadrapada', 'Revati'
]

NAKSHATRA_LORDS = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
]

# Exaltation & Debilitation Degrees
EXALTATION_DEGREES = {
    'Sun': 10.0,      # Aries 10°
    'Moon': 33.0,     # Taurus 3°
    'Mars': 298.0,    # Capricorn 28°
    'Mercury': 165.0, # Virgo 15°
    'Jupiter': 95.0,  # Cancer 5°
    'Venus': 357.0,   # Pisces 27°
    'Saturn': 200.0,  # Libra 20°
    'Rahu': 45.0,     # Taurus 15°
    'Ketu': 225.0     # Scorpio 15°
}

DEBILITATION_DEGREES = {
    'Sun': 190.0,     # Libra 10°
    'Moon': 213.0,    # Scorpio 3°
    'Mars': 118.0,    # Cancer 28°
    'Mercury': 345.0, # Pisces 15°
    'Jupiter': 275.0, # Capricorn 5°
    'Venus': 177.0,   # Virgo 27°
    'Saturn': 20.0,   # Aries 20°
    'Rahu': 225.0,    # Scorpio 15°
    'Ketu': 45.0      # Taurus 15°
}

# Combustion Distance Limits (Degrees from Sun)
COMBUST_LIMITS = {
    'Moon': 12.0,
    'Mars': 17.0,
    'Mercury': 14.0, # 12 if Retrograde
    'Jupiter': 11.0,
    'Venus': 10.0,   # 8 if Retrograde
    'Saturn': 15.0
}

# Natural Relationships (Friends, Neutral, Enemies)
NATURAL_FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'],
    'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus'],
    'Rahu': ['Mercury', 'Venus', 'Saturn'],
    'Ketu': ['Mars', 'Venus', 'Saturn']
}

NATURAL_ENEMIES = {
    'Sun': ['Venus', 'Saturn', 'Rahu', 'Ketu'],
    'Moon': ['Rahu', 'Ketu'],
    'Mars': ['Mercury', 'Rahu'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon', 'Mars'],
    'Rahu': ['Sun', 'Moon', 'Mars'],
    'Ketu': ['Sun', 'Moon']
}

if HAS_SWISSEPH:
    SWE_BODY_MAP = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO
    }
else:
    SWE_BODY_MAP = {}


@dataclass
class PlanetPosition:
    name: str
    tropical_lon: float
    sidereal_lon: float
    latitude: float
    declination: float
    distance: float
    speed: float
    is_retrograde: bool
    sign_index: int
    sign_name: str
    sign_lord: str
    sign_degree: float
    nakshatra_index: int
    nakshatra_name: str
    nakshatra_lord: str
    pada: int
    sub_lord: str
    sub_sub_lord: str
    is_combust: bool = False
    is_cazimi: bool = False
    exaltation_state: str = "Neutral" # Exalted, Debilitated, Moolatrikona, Swakshetra, Neutral
    dignity: str = "Neutral"         # Great Friend, Friend, Neutral, Enemy, Great Enemy

class PlanetEngine:
    """Calculates planetary positions, nakshatras, dignities, combustion, and aspects."""
    
    @staticmethod
    def get_kp_sub_lords(longitude: float) -> Tuple[str, str]:
        """Determine KP Sub-Lord and Sub-Sub-Lord for a given sidereal longitude."""
        # Nakshatra span = 13° 20' = 800 minutes = 48000 seconds
        # Sub-lord divisions follow Vimshottari proportion (total 120 years)
        total_sec = (longitude % 360.0) * 3600.0
        nak_sec = 13.333333333333334 * 3600.0
        nak_idx = int(total_sec // nak_sec)
        rem_sec = total_sec % nak_sec
        
        main_lord = NAKSHATRA_LORDS[nak_idx % 27]
        lord_order = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        years = {'Ketu':7, 'Venus':20, 'Sun':6, 'Moon':10, 'Mars':7, 'Rahu':18, 'Jupiter':16, 'Saturn':19, 'Mercury':17}
        
        start_idx = lord_order.index(main_lord)
        curr_sec = 0.0
        sub_lord = main_lord
        for i in range(9):
            p = lord_order[(start_idx + i) % 9]
            span = (years[p] / 120.0) * nak_sec
            if curr_sec <= rem_sec < (curr_sec + span):
                sub_lord = p
                rem_sec_sub = rem_sec - curr_sec
                sub_span = span
                # Sub-sub lord inside sub_lord
                sub_start_idx = lord_order.index(sub_lord)
                curr_sub_sec = 0.0
                sub_sub_lord = sub_lord
                for j in range(9):
                    p2 = lord_order[(sub_start_idx + j) % 9]
                    span2 = (years[p2] / 120.0) * sub_span
                    if curr_sub_sec <= rem_sec_sub < (curr_sub_sec + span2):
                        sub_sub_lord = p2
                        break
                    curr_sub_sec += span2
                return sub_lord, sub_sub_lord
            curr_sec += span
            
        return main_lord, main_lord

    @classmethod
    def calculate_planets(
        cls,
        jd_ut: float,
        ayanamsa_val: float,
        node_type: str = "True"
    ) -> Dict[str, PlanetPosition]:
        """Compute ephemeris positions for all planets."""
        planets_data: Dict[str, PlanetPosition] = {}
        
        if HAS_SWISSEPH:
            flags = swe.FLG_SPEED
            for p_name, swe_code in SWE_BODY_MAP.items():
                res, _ = swe.calc_ut(jd_ut, swe_code, flags)
                trop_lon = res[0] % 360.0
                lat = res[1]
                dist = res[2]
                speed = res[3]
                eq_res, _ = swe.calc_ut(jd_ut, swe_code, flags | swe.FLG_EQUATORIAL)
                dec = eq_res[1]
                sid_lon = (trop_lon - ayanamsa_val) % 360.0
                is_retro = speed < 0
                
                sign_idx = int(sid_lon // 30)
                sign_name = SIGN_NAMES[sign_idx]
                sign_lord = SIGN_LORDS[sign_name]
                sign_deg = sid_lon % 30.0
                
                nak_idx = int(sid_lon // (360.0 / 27.0))
                nak_name = NAKSHATRAS[nak_idx % 27]
                nak_lord = NAKSHATRA_LORDS[nak_idx % 27]
                pada = int((sid_lon % (360.0 / 27.0)) // (360.0 / 108.0)) + 1
                sub_lord, sub_sub_lord = cls.get_kp_sub_lords(sid_lon)
                
                planets_data[p_name] = PlanetPosition(
                    name=p_name,
                    tropical_lon=trop_lon,
                    sidereal_lon=sid_lon,
                    latitude=lat,
                    declination=dec,
                    distance=dist,
                    speed=speed,
                    is_retrograde=is_retro,
                    sign_index=sign_idx,
                    sign_name=sign_name,
                    sign_lord=sign_lord,
                    sign_degree=sign_deg,
                    nakshatra_index=nak_idx % 27,
                    nakshatra_name=nak_name,
                    nakshatra_lord=nak_lord,
                    pada=pada,
                    sub_lord=sub_lord,
                    sub_sub_lord=sub_sub_lord
                )

            # Rahu and Ketu
            node_code = swe.TRUE_NODE if node_type == "True" else swe.MEAN_NODE
            res_node, _ = swe.calc_ut(jd_ut, node_code, flags)
            rahu_trop = res_node[0] % 360.0
            rahu_speed = res_node[3]
            eq_node, _ = swe.calc_ut(jd_ut, node_code, flags | swe.FLG_EQUATORIAL)
            rahu_dec = eq_node[1]
            rahu_sid = (rahu_trop - ayanamsa_val) % 360.0
            ketu_sid = (rahu_sid + 180.0) % 360.0
            ketu_trop = (rahu_trop + 180.0) % 360.0
            
            # Rahu
            sign_idx = int(rahu_sid // 30)
            sign_name = SIGN_NAMES[sign_idx]
            nak_idx = int(rahu_sid // (360.0 / 27.0))
            sub_lord, sub_sub_lord = cls.get_kp_sub_lords(rahu_sid)
            planets_data['Rahu'] = PlanetPosition(
                name='Rahu', tropical_lon=rahu_trop, sidereal_lon=rahu_sid, latitude=res_node[1],
                declination=rahu_dec, distance=res_node[2], speed=rahu_speed, is_retrograde=rahu_speed < 0,
                sign_index=sign_idx, sign_name=sign_name, sign_lord=SIGN_LORDS[sign_name], sign_degree=rahu_sid % 30.0,
                nakshatra_index=nak_idx % 27, nakshatra_name=NAKSHATRAS[nak_idx % 27], nakshatra_lord=NAKSHATRA_LORDS[nak_idx % 27],
                pada=int((rahu_sid % (360.0 / 27.0)) // (360.0 / 108.0)) + 1, sub_lord=sub_lord, sub_sub_lord=sub_sub_lord
            )
            # Ketu
            sign_idx = int(ketu_sid // 30)
            sign_name = SIGN_NAMES[sign_idx]
            nak_idx = int(ketu_sid // (360.0 / 27.0))
            sub_lord, sub_sub_lord = cls.get_kp_sub_lords(ketu_sid)
            planets_data['Ketu'] = PlanetPosition(
                name='Ketu', tropical_lon=ketu_trop, sidereal_lon=ketu_sid, latitude=-res_node[1],
                declination=-rahu_dec, distance=res_node[2], speed=rahu_speed, is_retrograde=rahu_speed < 0,
                sign_index=sign_idx, sign_name=sign_name, sign_lord=SIGN_LORDS[sign_name], sign_degree=ketu_sid % 30.0,
                nakshatra_index=nak_idx % 27, nakshatra_name=NAKSHATRAS[nak_idx % 27], nakshatra_lord=NAKSHATRA_LORDS[nak_idx % 27],
                pada=int((ketu_sid % (360.0 / 27.0)) // (360.0 / 108.0)) + 1, sub_lord=sub_lord, sub_sub_lord=sub_sub_lord
            )
        else:
            # Pure Mathematical Mean Motion Fallback
            T = (jd_ut - 2451545.0) / 36525.0
            mean_rates = {
                'Sun': (280.46646 + 36000.76983 * T, 0.9856),
                'Moon': (218.3165 + 481267.8813 * T, 13.1763),
                'Mars': (355.453 + 19140.3026 * T, 0.5240),
                'Mercury': (252.251 + 149472.674 * T, 4.0923),
                'Jupiter': (34.404 + 3034.7925 * T, 0.0831),
                'Venus': (181.979 + 58517.8156 * T, 1.6021),
                'Saturn': (50.078 + 1222.1138 * T, 0.0335),
                'Rahu': (125.0445 - 1934.1363 * T, -0.0529)
            }
            mean_rates['Ketu'] = ((mean_rates['Rahu'][0] + 180.0) % 360.0, -0.0529)
            
            for p_name, (trop_l, spd) in mean_rates.items():
                trop_lon = trop_l % 360.0
                sid_lon = (trop_lon - ayanamsa_val + 360.0) % 360.0
                sign_idx = int(sid_lon // 30)
                sign_name = SIGN_NAMES[sign_idx]
                nak_idx = int(sid_lon // (360.0 / 27.0))
                sub_lord, sub_sub_lord = cls.get_kp_sub_lords(sid_lon)
                
                planets_data[p_name] = PlanetPosition(
                    name=p_name, tropical_lon=trop_lon, sidereal_lon=sid_lon, latitude=0.0,
                    declination=0.0, distance=1.0, speed=spd, is_retrograde=spd < 0,
                    sign_index=sign_idx, sign_name=sign_name, sign_lord=SIGN_LORDS[sign_name], sign_degree=sid_lon % 30.0,
                    nakshatra_index=nak_idx % 27, nakshatra_name=NAKSHATRAS[nak_idx % 27], nakshatra_lord=NAKSHATRA_LORDS[nak_idx % 27],
                    pada=int((sid_lon % (360.0 / 27.0)) // (360.0 / 108.0)) + 1, sub_lord=sub_lord, sub_sub_lord=sub_sub_lord
                )


        # 3. Check Combustion, Cazimi, Exaltation/Debilitation & Dignities
        sun_lon = planets_data['Sun'].sidereal_lon
        for p_name, p_obj in planets_data.items():
            if p_name in ['Sun', 'Rahu', 'Ketu', 'Uranus', 'Neptune', 'Pluto']:
                continue
            
            # Angular distance to Sun
            ang_dist = min(abs(p_obj.sidereal_lon - sun_lon), 360.0 - abs(p_obj.sidereal_lon - sun_lon))
            
            # Cazimi: within 17 arcminutes = 0.2833 degrees
            if ang_dist <= (17.0 / 60.0):
                p_obj.is_cazimi = True
                p_obj.is_combust = False
            else:
                limit = COMBUST_LIMITS.get(p_name, 12.0)
                if p_name in ['Mercury', 'Venus'] and p_obj.is_retrograde:
                    limit -= 2.0
                if ang_dist <= limit:
                    p_obj.is_combust = True
            
            # Exaltation / Debilitation
            ex_deg = EXALTATION_DEGREES.get(p_name)
            deb_deg = DEBILITATION_DEGREES.get(p_name)
            if ex_deg is not None:
                dist_ex = min(abs(p_obj.sidereal_lon - ex_deg), 360.0 - abs(p_obj.sidereal_lon - ex_deg))
                dist_deb = min(abs(p_obj.sidereal_lon - deb_deg), 360.0 - abs(p_obj.sidereal_lon - deb_deg))
                if dist_ex <= 3.0:
                    p_obj.exaltation_state = "Exalted"
                elif dist_deb <= 3.0:
                    p_obj.exaltation_state = "Debilitated"
                elif p_obj.sign_lord == p_name:
                    p_obj.exaltation_state = "Swakshetra"
                else:
                    p_obj.exaltation_state = "Neutral"

        return planets_data
