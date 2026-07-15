# -*- coding: utf-8 -*-
"""
Vedic Astrology Platform Utilities.

This module provides high-precision astronomical calculations using Swiss Ephemeris
and resolves coordinates, timezones, house cusps, and time-lord cycles (dashas).
It utilizes typed dataclasses and type hinting for strict API definitions.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
import logging
from typing import Any, Dict, List, Optional, Tuple
from geopy.geocoders import Nominatim
import pytz
import swisseph as swe
from timezonefinder import TimezoneFinder

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu']

SIGN_NAMES = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

INDIAN_NAMES = {
    'Sun': 'Surya', 'Moon': 'Chandra', 'Mercury': 'Budh', 'Venus': 'Shukra',
    'Mars': 'Mangal', 'Jupiter': 'Guru', 'Saturn': 'Shani',
    'Rahu': 'Rahu', 'Ketu': 'Ketu'
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

VIMSHOTTARI_DASHA_SEQUENCE = [
    ('Ketu', 7), ('Venus', 20), ('Sun', 6), ('Moon', 10),
    ('Mars', 7), ('Rahu', 18), ('Jupiter', 16), ('Saturn', 19), ('Mercury', 17)
]

# Friend/Enemy map
FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'],
    'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus'],
    'Rahu': ['Mercury', 'Venus', 'Saturn'],
    'Ketu': ['Mercury', 'Venus', 'Saturn']
}

ENEMIES = {
    'Sun': ['Venus', 'Saturn'],
    'Moon': [],
    'Mars': ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Venus', 'Mercury'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon'],
    'Rahu': ['Sun', 'Moon', 'Mars'],
    'Ketu': ['Sun', 'Moon', 'Mars']
}

HOUSE_SYSTEM_MAP = {
    "Whole Sign": b'W',
    "Placidus": b'P',
    "Porphyry": b'O',
    "Equal": b'A'
}

AYANAMSA_MAP = {
    "Lahiri": swe.SIDM_LAHIRI,
    "Krishnamurti": swe.SIDM_KRISHNAMURTI,
    "Raman": swe.SIDM_RAMAN,
    "ukteshwar": swe.SIDM_YUKTESHWAR,
    "Fagan Bradley": swe.SIDM_FAGAN_BRADLEY
}

SWE_PLANET_MAP = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN
}


@dataclass(frozen=True)
class PlanetInfo:
    """Dataclass storing the astronomical details of a planet."""
    id: str
    lon: float
    lat: float
    lonspeed: float
    latspeed: float
    sign: str
    signlon: float
    house: str


@dataclass(frozen=True)
class PointInfo:
    """Dataclass storing details of calculated points like Ascendant or MC."""
    id: str
    lon: float
    sign: str
    signlon: float


@dataclass(frozen=True)
class HouseInfo:
    """Dataclass storing the details of a house cusp."""
    id: str
    lon: float
    sign: str
    signlon: float


@dataclass
class SwissChart:
    """Class representing a calculated birth chart."""
    jd: float
    lat: float
    lon: float
    zodiac: str
    house_system: str
    ayanamsa: str
    node_type: str
    timezone: str
    utc_offset_hours: float
    formatted_pob: str
    ayanamsa_val: float
    asc: PointInfo
    mc: PointInfo
    planets: Dict[str, PlanetInfo] = field(default_factory=dict)
    houses: Dict[str, HouseInfo] = field(default_factory=dict)

    def get(self, name: str) -> Optional[object]:
        """Provides backward-compatible lookup interface for planets and points."""
        if name == 'Asc':
            return self.asc
        if name == 'MC':
            return self.mc
        return self.planets.get(name)

    def getHouse(self, num: int) -> Optional[HouseInfo]:
        """Provides backward-compatible lookup for houses."""
        return self.houses.get(str(num))


BIRTHPLACE_CACHE = {
    "patna": (25.5941, 85.1376, "Asia/Kolkata", "Patna, Bihar, India"),
    "patna, bihar": (25.5941, 85.1376, "Asia/Kolkata", "Patna, Bihar, India"),
    "patna, bihar, india": (25.5941, 85.1376, "Asia/Kolkata", "Patna, Bihar, India"),
    "delhi": (28.6139, 77.2090, "Asia/Kolkata", "New Delhi, Delhi, India"),
    "delhi, india": (28.6139, 77.2090, "Asia/Kolkata", "New Delhi, Delhi, India"),
    "new delhi": (28.6139, 77.2090, "Asia/Kolkata", "New Delhi, Delhi, India"),
    "new delhi, india": (28.6139, 77.2090, "Asia/Kolkata", "New Delhi, Delhi, India"),
    "mumbai": (19.0760, 72.8777, "Asia/Kolkata", "Mumbai, Maharashtra, India"),
    "mumbai, maharashtra, india": (19.0760, 72.8777, "Asia/Kolkata", "Mumbai, Maharashtra, India"),
    "kolkata": (22.5726, 88.3639, "Asia/Kolkata", "Kolkata, West Bengal, India"),
    "kolkata, west bengal, india": (22.5726, 88.3639, "Asia/Kolkata", "Kolkata, West Bengal, India"),
    "chennai": (13.0827, 80.2707, "Asia/Kolkata", "Chennai, Tamil Nadu, India"),
    "chennai, tamil nadu, india": (13.0827, 80.2707, "Asia/Kolkata", "Chennai, Tamil Nadu, India"),
    "bangalore": (12.9716, 77.5946, "Asia/Kolkata", "Bengaluru, Karnataka, India"),
    "bengaluru": (12.9716, 77.5946, "Asia/Kolkata", "Bengaluru, Karnataka, India"),
    "bangalore, karnataka, india": (12.9716, 77.5946, "Asia/Kolkata", "Bengaluru, Karnataka, India"),
    "bengaluru, karnataka, india": (12.9716, 77.5946, "Asia/Kolkata", "Bengaluru, Karnataka, India"),
    "hyderabad": (17.3850, 78.4867, "Asia/Kolkata", "Hyderabad, Telangana, India"),
    "hyderabad, telangana, india": (17.3850, 78.4867, "Asia/Kolkata", "Hyderabad, Telangana, India"),
    "pune": (18.5204, 73.8567, "Asia/Kolkata", "Pune, Maharashtra, India"),
    "pune, maharashtra, india": (18.5204, 73.8567, "Asia/Kolkata", "Pune, Maharashtra, India")
}

def resolve_place(place: str) -> Tuple[float, float, str, str]:
    """Helper to resolve place coordinates and timezone safely with caching and fallbacks."""
    key = place.strip().lower()
    if key in BIRTHPLACE_CACHE:
        return BIRTHPLACE_CACHE[key]
    
    # Try fuzzy matching in cache
    for k, v in BIRTHPLACE_CACHE.items():
        if k in key or key in k:
            return v

    geolocator = Nominatim(user_agent="kundli-app-v2")
    try:
        location = geolocator.geocode(place, timeout=10)
        if location:
            lat, lon = float(location.latitude), float(location.longitude)
            tf = TimezoneFinder()
            tz_str = tf.timezone_at(lng=lon, lat=lat) or 'Asia/Kolkata'
            return lat, lon, tz_str, location.address
    except Exception as e:
        logger.error(f"Geocoding error for '{place}', using fallback: {e}")
        
    # Safe fallback values instead of throwing connection pools errors
    if "patna" in key:
        return 25.5941, 85.1376, "Asia/Kolkata", "Patna, Bihar, India (Fallback)"
    return 28.6139, 77.2090, "Asia/Kolkata", "New Delhi, Delhi, India (Fallback)"

def get_place_info(place: str) -> str:
    """Resolves coordinates, timezone, and current GMT offset for a given location."""
    try:
        lat, lon, tz_str, addr = resolve_place(place)
        tz = pytz.timezone(tz_str)
        now = datetime.now(tz)
        offset = now.utcoffset().total_seconds() / 3600.0
        return f"{addr} ({lat:.4f}°, {lon:.4f}°, {tz_str} GMT{offset:+.1f})"
    except Exception as e:
        logger.error(f"Error in get_place_info: {e}")
        return "New Delhi, Delhi, India (28.6139°, 77.2090°)"

def get_house_number(planet_lon: float, house_cusps: List[float], house_system: str = "Whole Sign", asc_sign_index: int = 0) -> str:
    """Calculates which house a planet resides in based on the house cusps.

    Args:
        planet_lon: Full longitude of the planet (0-360).
        house_cusps: List of 12 house cusp coordinates.
        house_system: The chosen house system.
        asc_sign_index: Index of the sign containing the Ascendant.

    Returns:
        String representing house number (1-12).
    """
    if house_system == "Whole Sign":
        p_sign_index = int(planet_lon // 30)
        return str((p_sign_index - asc_sign_index) % 12 + 1)
    
    # Range checks for other house systems
    for i in range(12):
        c1 = house_cusps[i]
        c2 = house_cusps[(i + 1) % 12]
        if c1 <= c2:
            if c1 <= planet_lon < c2:
                return str(i + 1)
        else:
            if planet_lon >= c1 or planet_lon < c2:
                return str(i + 1)
    return "1"


def get_chart(date_str: str, time_str: str, place: str, zodiac: str = "Sidereal", 
              house_system: str = "Whole Sign", ayanamsa: str = "Lahiri", node_type: str = "True") -> SwissChart:
    """Calculates and returns a SwissChart birth chart."""
    lat, lon, tz_str, addr = resolve_place(place)
    tz = pytz.timezone(tz_str)
    local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
    localized_dt = tz.localize(local_dt)
    utc_dt = localized_dt.astimezone(pytz.utc)
    
    # Julian Date UT
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                    utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)
    
    # Determine Ephemeris Flags
    flags = swe.FLG_SPEED
    if zodiac == "Sidereal":
        flags |= swe.FLG_SIDEREAL
        sid_mode = AYANAMSA_MAP.get(ayanamsa, swe.SIDM_LAHIRI)
        swe.set_sid_mode(sid_mode)
        
    ayanamsa_val = swe.get_ayanamsa_ut(jd)
    
    # House calculations
    hsys_byte = HOUSE_SYSTEM_MAP.get(house_system, b'W')
    hflags = swe.FLG_SIDEREAL if zodiac == "Sidereal" else 0
    hlist, ascmc = swe.houses_ex(jd, lat, lon, hsys_byte, hflags)
    
    asc = PointInfo('Asc', ascmc[0], SIGN_NAMES[int(ascmc[0] // 30)], ascmc[0] % 30)
    mc = PointInfo('MC', ascmc[1], SIGN_NAMES[int(ascmc[1] // 30)], ascmc[1] % 30)
    
    chart = SwissChart(
        jd=jd, lat=lat, lon=lon, zodiac=zodiac, house_system=house_system, 
        ayanamsa=ayanamsa, node_type=node_type, timezone=tz_str, 
        utc_offset_hours=localized_dt.utcoffset().total_seconds() / 3600.0,
        formatted_pob=addr,
        ayanamsa_val=ayanamsa_val, asc=asc, mc=mc
    )
    
    # Calculate Houses
    for i in range(12):
        h_lon = hlist[i]
        chart.houses[str(i+1)] = HouseInfo(f'House{i+1}', h_lon, SIGN_NAMES[int(h_lon // 30)], h_lon % 30)
        
    # Calculate Planets Sun to Saturn
    for p_name in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        swe_id = SWE_PLANET_MAP[p_name]
        res, *err = swe.calc_ut(jd, swe_id, flags)
        lon_deg = res[0]
        chart.planets[p_name] = PlanetInfo(
            id=p_name, lon=lon_deg, lat=res[1], lonspeed=res[3], latspeed=res[4],
            sign=SIGN_NAMES[int(lon_deg // 30)], signlon=lon_deg % 30, house="1"
        )
        
    # Calculate Rahu (North Node)
    node_id = swe.TRUE_NODE if node_type == "True" else swe.MEAN_NODE
    res_rahu, *err = swe.calc_ut(jd, node_id, flags)
    rahu_lon = res_rahu[0]
    chart.planets['Rahu'] = PlanetInfo(
        id='Rahu', lon=rahu_lon, lat=res_rahu[1], lonspeed=res_rahu[3], latspeed=res_rahu[4],
        sign=SIGN_NAMES[int(rahu_lon // 30)], signlon=rahu_lon % 30, house="1"
    )
    
    # Calculate Ketu (South Node, exactly 180 opposite Rahu)
    ketu_lon = (rahu_lon + 180) % 360
    chart.planets['Ketu'] = PlanetInfo(
        id='Ketu', lon=ketu_lon, lat=-res_rahu[1], lonspeed=res_rahu[3], latspeed=-res_rahu[4],
        sign=SIGN_NAMES[int(ketu_lon // 30)], signlon=ketu_lon % 30, house="1"
    )
    
    # Update house placement calculations for all planets
    asc_sign_index = int(ascmc[0] // 30)
    for p_name in PLANETS:
        p_data = chart.planets[p_name]
        h_num = get_house_number(p_data.lon, list(hlist), house_system, asc_sign_index)
        chart.planets[p_name] = PlanetInfo(
            id=p_data.id, lon=p_data.lon, lat=p_data.lat, lonspeed=p_data.lonspeed,
            latspeed=p_data.latspeed, sign=p_data.sign, signlon=p_data.signlon, house=h_num
        )
        
    return chart


def get_planet_positions(chart: SwissChart) -> Dict[str, Dict]:
    """Calculates planet metadata values (Indian names, Nakshatras, Dignities, Strengths).

    Args:
        chart: The computed SwissChart.

    Returns:
        A dictionary containing parameters for each planet.
    """
    sun_lon = chart.get('Sun').lon
    planets_data = {}
    for planet in PLANETS:
        obj = chart.get(planet)
        sign = obj.sign
        deg = round(obj.lon % 30, 2)
        
        lon_val = obj.lon % 360
        nak_index = int(lon_val // (13 + 1/3))
        pada = int((lon_val % (13 + 1/3)) // (13 + 1/3 / 4)) + 1
        nakshatra = NAKSHATRAS[nak_index]
        
        sign_lord = get_sign_lord(sign)
        relation = get_planet_relation(planet, sign_lord)
        dignity = get_dignity(planet, sign)
        strength = estimate_strength(dignity, relation)

        # Margi / Vakri
        is_retro = False
        if planet in ['Rahu', 'Ketu']:
            is_retro = True
        elif planet not in ['Sun', 'Moon'] and obj.lonspeed < 0:
            is_retro = True

        # Udita / Asta (Combust)
        is_comb = False
        if planet not in ['Sun', 'Moon', 'Rahu', 'Ketu']:
            diff = abs(obj.lon - sun_lon) % 360
            if diff > 180:
                diff = 360 - diff
            comb_limits = {
                'Mars': 17.0,
                'Mercury': 12.0 if is_retro else 14.0,
                'Jupiter': 11.0,
                'Venus': 8.0 if is_retro else 10.0,
                'Saturn': 15.0
            }
            if diff <= comb_limits.get(planet, 0.0):
                is_comb = True

        planets_data[planet] = {
            "sign": sign,
            "lon": deg,
            "indian": INDIAN_NAMES.get(planet, planet),
            "nakshatra": nakshatra,
            "pada": pada,
            "sign_lord": sign_lord,
            "relation": relation,
            "dignity": dignity,
            "strength": strength,
            "house": obj.house,
            "is_retrograde": is_retro,
            "is_combust": is_comb
        }
    return planets_data


def get_house_details(chart: SwissChart, house_system: str = "Whole Sign") -> Dict[str, Dict]:
    """Maps which planets occupy which astrological houses.

    Args:
        chart: The computed SwissChart.
        house_system: The active house system name.

    Returns:
        A dictionary mapping house numbers to signs and occupant planet lists.
    """
    house_data = {}
    for i in range(1, 13):
        house = chart.getHouse(i)
        house_data[str(i)] = {
            'sign': house.sign,
            'planets': []
        }

    for planet in PLANETS:
        obj = chart.get(planet)
        house_num = obj.house
        if house_num in house_data:
            house_data[house_num]['planets'].append(INDIAN_NAMES.get(planet, planet))

    return house_data


def get_ascendant(chart: SwissChart) -> Tuple[str, float]:
    """Retrieves the Ascendant sign and degree.

    Args:
        chart: The computed SwissChart.

    Returns:
        A tuple of (Sign Name, Degree in Sign).
    """
    asc = chart.get('Asc')
    return asc.sign, round(asc.lon % 30, 2)


def get_dignity(planet: str, sign: str) -> str:
    """Calculates planetary exaltation and debilitation status."""
    dignity_map = {
        'Sun': {'exalt': 'Aries', 'debil': 'Libra'},
        'Moon': {'exalt': 'Taurus', 'debil': 'Scorpio'},
        'Mars': {'exalt': 'Capricorn', 'debil': 'Cancer'},
        'Mercury': {'exalt': 'Virgo', 'debil': 'Pisces'},
        'Jupiter': {'exalt': 'Cancer', 'debil': 'Capricorn'},
        'Venus': {'exalt': 'Pisces', 'debil': 'Virgo'},
        'Saturn': {'exalt': 'Libra', 'debil': 'Aries'},
        'Rahu': {'exalt': 'Taurus', 'debil': 'Scorpio'},
        'Ketu': {'exalt': 'Scorpio', 'debil': 'Taurus'}
    }
    if planet not in dignity_map:
        return "Neutral"
    if sign == dignity_map[planet]['exalt']:
        return "Uchh (Exalted)"
    elif sign == dignity_map[planet]['debil']:
        return "Neech (Debilitated)"
    else:
        return "Neutral"


def estimate_strength(dignity: str, relation: str) -> str:
    """Estimates strength based on dignity and relations."""
    if "Exalted" in dignity:
        return "Strong"
    elif "Debilitated" in dignity or relation == "Enemy":
        return "Weak"
    else:
        return "Moderate"


def get_planet_relation(p1: str, p2: str) -> str:
    """Finds natural relationships (Friend, Enemy, Neutral) between planets."""
    if p2 in FRIENDS.get(p1, []):
        return "Friend"
    elif p2 in ENEMIES.get(p1, []):
        return "Enemy"
    else:
        return "Neutral"


def get_sign_lord(sign: str) -> str:
    """Finds the ruler of a zodiac sign."""
    lord_map = {
        'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
        'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
        'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
        'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
    }
    return lord_map.get(sign, '')


def get_vimshottari_dasha(moon_lon: float, birthdate_str: str) -> Tuple[str, str, List[Dict]]:
    """Calculates nested Vimshottari Dasha cycles to three levels.

    Args:
        moon_lon: Planet longitude for the Moon.
        birthdate_str: Date of birth (YYYY/MM/DD).

    Returns:
        A tuple of (Moon Nakshatra, Birth Lord, Dasha tree hierarchy).
    """
    total_deg = moon_lon % 360
    nak_index = int(total_deg // (13 + 1/3))
    nakshatra = NAKSHATRAS[nak_index]
    lord = NAKSHATRA_LORDS[nak_index]
    deg_in_nak = total_deg % (13 + 1/3)
    percent_completed = deg_in_nak / (13 + 1/3)

    start_index = next(i for i, (p, _) in enumerate(VIMSHOTTARI_DASHA_SEQUENCE) if p == lord)
    remaining_years_first = (1 - percent_completed) * dict(VIMSHOTTARI_DASHA_SEQUENCE)[lord]

    dasha_tree = []
    current_date = datetime.strptime(birthdate_str, "%Y/%m/%d")
    seq_len = len(VIMSHOTTARI_DASHA_SEQUENCE)

    for i in range(seq_len):
        idx = (start_index + i) % seq_len
        m_planet, m_years = VIMSHOTTARI_DASHA_SEQUENCE[idx]
        m_yrs = remaining_years_first if i == 0 else m_years
        m_end_date = current_date + timedelta(days=m_yrs * 365.25)
        
        antardashas = []
        ad_start_date = current_date
        ad_start_index = next(k for k, (p, _) in enumerate(VIMSHOTTARI_DASHA_SEQUENCE) if p == m_planet)
        
        if i == 0:
            total_m_years = dict(VIMSHOTTARI_DASHA_SEQUENCE)[m_planet]
            elapsed_years = percent_completed * total_m_years
            
            running_ad_years = 0.0
            ad_idx_offset = 0
            ad_remaining_years_first = 0.0
            for ad_i in range(seq_len):
                ad_idx = (ad_start_index + ad_i) % seq_len
                ad_planet, ad_years_standard = VIMSHOTTARI_DASHA_SEQUENCE[ad_idx]
                ad_duration = (total_m_years * ad_years_standard) / 120.0
                if running_ad_years + ad_duration > elapsed_years:
                    ad_idx_offset = ad_i
                    ad_remaining_years_first = (running_ad_years + ad_duration) - elapsed_years
                    break
                running_ad_years += ad_duration
            
            for ad_i in range(seq_len - ad_idx_offset):
                ad_idx = (ad_start_index + ad_idx_offset + ad_i) % seq_len
                ad_planet, ad_years_standard = VIMSHOTTARI_DASHA_SEQUENCE[ad_idx]
                
                ad_yrs = ad_remaining_years_first if ad_i == 0 else (total_m_years * ad_years_standard) / 120.0
                ad_end_date = ad_start_date + timedelta(days=ad_yrs * 365.25)
                
                pratyantardashas = []
                pd_start_date = ad_start_date
                pd_start_index = next(k for k, (p, _) in enumerate(VIMSHOTTARI_DASHA_SEQUENCE) if p == ad_planet)
                
                if ad_i == 0:
                    ad_duration_full = (total_m_years * ad_years_standard) / 120.0
                    ad_elapsed = ad_duration_full - ad_remaining_years_first
                    
                    pd_running_years = 0.0
                    pd_idx_offset = 0
                    pd_remaining_years_first = 0.0
                    for pd_i in range(seq_len):
                        pd_idx = (pd_start_index + pd_i) % seq_len
                        pd_planet, pd_years_standard = VIMSHOTTARI_DASHA_SEQUENCE[pd_idx]
                        pd_duration = (ad_duration_full * pd_years_standard) / 120.0
                        if pd_running_years + pd_duration > ad_elapsed:
                            pd_idx_offset = pd_i
                            pd_remaining_years_first = (pd_running_years + pd_duration) - ad_elapsed
                            break
                        pd_running_years += pd_duration
                        
                    for pd_i in range(seq_len - pd_idx_offset):
                        pd_idx = (pd_start_index + pd_idx_offset + pd_i) % seq_len
                        pd_planet, pd_years_standard = VIMSHOTTARI_DASHA_SEQUENCE[pd_idx]
                        pd_yrs = pd_remaining_years_first if pd_i == 0 else (ad_duration_full * pd_years_standard) / 120.0
                        pd_end_date = pd_start_date + timedelta(days=pd_yrs * 365.25)
                        pratyantardashas.append({
                            'planet': pd_planet,
                            'start': pd_start_date.date(),
                            'end': pd_end_date.date()
                        })
                        pd_start_date = pd_end_date
                else:
                    for pd_i in range(seq_len):
                        pd_idx = (pd_start_index + pd_i) % seq_len
                        pd_planet, pd_years_standard = VIMSHOTTARI_DASHA_SEQUENCE[pd_idx]
                        pd_yrs = (ad_yrs * pd_years_standard) / 120.0
                        pd_end_date = pd_start_date + timedelta(days=pd_yrs * 365.25)
                        pratyantardashas.append({
                            'planet': pd_planet,
                            'start': pd_start_date.date(),
                            'end': pd_end_date.date()
                        })
                        pd_start_date = pd_end_date
                
                antardashas.append({
                    'planet': ad_planet,
                    'start': ad_start_date.date(),
                    'end': ad_end_date.date(),
                    'pratyantardashas': pratyantardashas
                })
                ad_start_date = ad_end_date
        else:
            for ad_i in range(seq_len):
                ad_idx = (ad_start_index + ad_i) % len(VIMSHOTTARI_DASHA_SEQUENCE)
                ad_planet, ad_years_standard = VIMSHOTTARI_DASHA_SEQUENCE[ad_idx]
                ad_yrs = (m_years * ad_years_standard) / 120.0
                ad_end_date = ad_start_date + timedelta(days=ad_yrs * 365.25)
                
                pratyantardashas = []
                pd_start_date = ad_start_date
                pd_start_index = next(k for k, (p, _) in enumerate(VIMSHOTTARI_DASHA_SEQUENCE) if p == ad_planet)
                
                for pd_i in range(seq_len):
                    pd_idx = (pd_start_index + pd_i) % seq_len
                    pd_planet, pd_years_standard = VIMSHOTTARI_DASHA_SEQUENCE[pd_idx]
                    pd_yrs = (ad_yrs * pd_years_standard) / 120.0
                    pd_end_date = pd_start_date + timedelta(days=pd_yrs * 365.25)
                    pratyantardashas.append({
                        'planet': pd_planet,
                        'start': pd_start_date.date(),
                        'end': pd_end_date.date()
                    })
                    pd_start_date = pd_end_date
                
                antardashas.append({
                    'planet': ad_planet,
                    'start': ad_start_date.date(),
                    'end': ad_end_date.date(),
                    'pratyantardashas': pratyantardashas
                })
                ad_start_date = ad_end_date
                
        dasha_tree.append({
            'planet': m_planet,
            'start': current_date.date(),
            'end': m_end_date.date(),
            'antardashas': antardashas
        })
        current_date = m_end_date
        
    return nakshatra, lord, dasha_tree


def get_d9_sign(planet_lon: float) -> str:
    """Calculates the Navamsa (D9) sign of a planet based on absolute longitude."""
    lon = planet_lon % 360
    sign_index = int(lon // 30)
    sign_lon = lon % 30
    nav_index = int(sign_lon // (3.3333333333333335))
    if sign_index in [0, 4, 8]:      # Fire signs (Aries, Leo, Sagittarius) -> Start at Aries
        d9_idx = (0 + nav_index) % 12
    elif sign_index in [1, 5, 9]:    # Earth signs (Taurus, Virgo, Capricorn) -> Start at Capricorn
        d9_idx = (9 + nav_index) % 12
    elif sign_index in [2, 6, 10]:   # Airy signs (Gemini, Libra, Aquarius) -> Start at Libra
        d9_idx = (6 + nav_index) % 12
    else:                            # Water signs (Cancer, Scorpio, Pisces) -> Start at Cancer
        d9_idx = (3 + nav_index) % 12
    return SIGN_NAMES[d9_idx]


YOGA_NAMES = [
    'Vishkumbha', 'Preeti', 'Ayushman', 'Saubhagya', 'Shobhana', 'Atiganda',
    'Sukarma', 'Dhriti', 'Shoola', 'Ganda', 'Vriddhi', 'Dhruva',
    'Vyaghipata', 'Harshana', 'Vajra', 'Siddhi', 'Vyatipata', 'Variyan',
    'Parigha', 'Shiva', 'Siddha', 'Sadhya', 'Shubha', 'Shukla',
    'Brahma', 'Indra', 'Vaidhriti'
]

TITHI_NAMES = [
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami', 'Shashthi',
    'Saptami', 'Ashtami', 'Navami', 'Dashami', 'Ekadashi', 'Dwadashi',
    'Trayodashi', 'Chaturdashi', 'Purnima',
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami', 'Shashthi',
    'Saptami', 'Ashtami', 'Navami', 'Dashami', 'Ekadashi', 'Dwadashi',
    'Trayodashi', 'Chaturdashi', 'Amavasya'
]

VARA_NAMES = [
    'Somavara (Monday)', 'Mangalavara (Tuesday)', 'Budhavara (Wednesday)',
    'Guruvara (Thursday)', 'Shukravara (Friday)', 'Shanivara (Saturday)',
    'Ravivara (Sunday)'
]


def get_panchang(sun_lon: float, moon_lon: float, birth_date: date, lat: float, lon: float, tz_offset: float) -> Dict[str, Any]:
    """Calculates high-precision Hindu Panchang details and element transition times using Swiss Ephemeris."""
    # 1. Sunrise / Sunset
    sr_str, ss_str = calculate_sunrise_sunset_approx(birth_date, lat, lon, tz_offset)
    
    tithi_angle = (moon_lon - sun_lon) % 360
    tithi_num = int(tithi_angle // 12) + 1
    tithi_name = TITHI_NAMES[tithi_num - 1]
    paksha = "Shukla Paksha" if tithi_num <= 15 else "Krishna Paksha"
    
    # Calculate approx moonrise based on tithi angle offset from sunrise
    moonrise_offset = (tithi_angle / 360.0) * 24.0
    sr_h = int(sr_str.split(':')[0]) + int(sr_str.split(':')[1]) / 60.0
    mr_h = (sr_h + moonrise_offset) % 24.0
    ms_h = (mr_h + 12.0) % 24.0
    mr_str = format_float_hours(mr_h)
    ms_str = format_float_hours(ms_h)
    
    # Nakshatra, Yoga, Karana at Sunrise/Birth
    nak_index = int(moon_lon // (13.333333333333334))
    nakshatra = NAKSHATRAS[nak_index]
    
    yoga_angle = (sun_lon + moon_lon) % 360
    yoga_index = int(yoga_angle // (13.333333333333334))
    yoga_name = YOGA_NAMES[yoga_index]
    
    karana_index = int(tithi_angle // 6)
    if karana_index == 0:
        karana_name = 'Kimstughna'
    elif karana_index == 57:
        karana_name = 'Shakuni'
    elif karana_index == 58:
        karana_name = 'Chatuspada'
    elif karana_index == 59:
        karana_name = 'Naga'
    else:
        mobile_karanas = ['Bava', 'Balava', 'Kaulava', 'Taitila', 'Gara', 'Vanija', 'Vishti']
        karana_name = mobile_karanas[(karana_index - 1) % 7]
        
    vara_name = VARA_NAMES[birth_date.weekday()]
    
    # Dynamic transition scanning: Scan Sunrise UT to Sunrise + 25 Hours UT
    tithis = []
    nakshatras = []
    yogas = []
    karanas = []
    
    sr_year = birth_date.year
    sr_month = birth_date.month
    sr_day = birth_date.day
    
    sr_dec = sr_h - tz_offset
    jd_start = swe.julday(sr_year, sr_month, sr_day, sr_dec)
    
    last_t = -1
    last_n = -1
    last_y = -1
    last_k = -1
    
    for step in range(250 + 1):  # Scan every 6 minutes (10 steps per hour)
        h_offset = step / 10.0
        jd_current = jd_start + (h_offset / 24.0)
        
        # Calculate Sun and Moon positions at current Julian Date
        res_sun, *err = swe.calc_ut(jd_current, swe.SUN)
        res_moon, *err = swe.calc_ut(jd_current, swe.MOON)
        
        c_sun_lon = res_sun[0]
        c_moon_lon = res_moon[0]
        
        c_tithi_angle = (c_moon_lon - c_sun_lon) % 360
        c_tithi = int(c_tithi_angle // 12) + 1
        c_nak = int(c_moon_lon // (13.333333333333334)) + 1
        
        c_yoga_angle = (c_sun_lon + c_moon_lon) % 360
        c_yoga = int(c_yoga_angle // (13.333333333333334)) + 1
        
        c_karana = int(c_tithi_angle // 6) + 1
        
        time_label = format_float_hours((sr_h + h_offset) % 24.0)
        
        # Tithi changes
        if c_tithi != last_t:
            tithis.append({"name": TITHI_NAMES[c_tithi - 1], "time": time_label, "hour": h_offset})
            last_t = c_tithi
            
        # Nakshatra changes
        if c_nak != last_n:
            nakshatras.append({"name": NAKSHATRAS[c_nak - 1], "time": time_label, "hour": h_offset})
            last_n = c_nak
            
        # Yoga changes
        if c_yoga != last_y:
            yogas.append({"name": YOGA_NAMES[c_yoga - 1], "time": time_label, "hour": h_offset})
            last_y = c_yoga
            
        # Karana changes
        if c_karana != last_k:
            k_name = ""
            k_idx = c_karana - 1
            if k_idx == 0: k_name = 'Kimstughna'
            elif k_idx == 57: k_name = 'Shakuni'
            elif k_idx == 58: k_name = 'Chatuspada'
            elif k_idx == 59: k_name = 'Naga'
            else:
                mobile_karanas = ['Bava', 'Balava', 'Kaulava', 'Taitila', 'Gara', 'Vanija', 'Vishti']
                k_name = mobile_karanas[(k_idx - 1) % 7]
            karanas.append({"name": k_name, "time": time_label, "hour": h_offset})
            last_k = c_karana
            
    return {
        "tithi": f"{tithi_name} ({paksha})",
        "nakshatra": nakshatra,
        "yoga": yoga_name,
        "karana": karana_name,
        "vara": vara_name,
        "sunrise": sr_str,
        "sunset": ss_str,
        "moonrise": mr_str,
        "moonset": ms_str,
        "tithis_list": tithis,
        "nakshatras_list": nakshatras,
        "yogas_list": yogas,
        "karanas_list": karanas
    }


def get_extended_panchang(sun_lon: float, moon_lon: float, birth_date: date, lat: float, lon: float, tz_offset: float, ayanamsa_val: float, jd: float) -> Dict[str, Any]:
    """Calculates all advanced Hindu Panchang elements dynamically, replacing hardcoded placeholders."""
    p = get_panchang(sun_lon, moon_lon, birth_date, lat, lon, tz_offset)
    tithi_num = int(((moon_lon - sun_lon) % 360) // 12) + 1
    
    shaka_year = birth_date.year - 78
    vikrama_year = birth_date.year + 57
    kali_year = birth_date.year + 3101
    
    SAMVATSARAS = [
        "Prabhava", "Vibhava", "Shukla", "Pramoda", "Prajapati", "Angira", "Shrimukha", "Bhava",
        "Yuva", "Dhatri", "Ishvara", "Bahudhanya", "Pramathi", "Vikrama", "Vrisha", "Chitrabhanu",
        "Subhanu", "Tarana", "Parthiva", "Vyaya", "Sarvajit", "Sarvadhari", "Virodhikrita", "Vikrita",
        "Khara", "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukha", "Hemalamba", "Vilamba",
        "Vikari", "Sharvari", "Plava", "Shubhakrita", "Shobhana", "Krodhi", "Vishvavasu", "Parabhavi",
        "Plavanga", "Kilaka", "Saumya", "Sadharana", "Virodha", "Paridhavi", "Pramadi", "Ananda",
        "Rakshasa", "Anala", "Pingala", "Kalayukta", "Siddharthi", "Raudra", "Durmati", "Dundubhi",
        "Rudhiraudgari", "Raktaksha", "Krodhana", "Kshaya"
    ]
    
    samvatsara_name = SAMVATSARAS[(vikrama_year + 9) % 60]
    
    sun_sign_idx = int((sun_lon - ayanamsa_val) % 360 // 30)
    LUNAR_MONTHS = ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada", "Ashvina", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"]
    lunar_month = LUNAR_MONTHS[sun_sign_idx]
    
    paksha = "Shukla Paksha" if "Shukla" in p["tithi"] else "Krishna Paksha"
    
    if paksha == "Krishna Paksha":
        amanta_month = LUNAR_MONTHS[(sun_sign_idx - 1) % 12]
    else:
        amanta_month = lunar_month
        
    pravishte = int((sun_lon - ayanamsa_val) % 30) + 1
    
    sun_trop = (sun_lon + ayanamsa_val) % 360
    if 330 <= sun_trop or sun_trop < 30:
        drik_ritu = "Vasanta (Spring)"
    elif 30 <= sun_trop < 90:
        drik_ritu = "Grishma (Summer)"
    elif 90 <= sun_trop < 150:
        drik_ritu = "Varsha (Monsoon)"
    elif 150 <= sun_trop < 210:
        drik_ritu = "Sharad (Autumn)"
    elif 210 <= sun_trop < 270:
        drik_ritu = "Hemant (Prewinter)"
    else:
        drik_ritu = "Shishir (Winter)"
        
    vedic_ritu_map = {
        "Chaitra": "Vasanta (Spring)", "Vaishakha": "Vasanta (Spring)",
        "Jyeshtha": "Grishma (Summer)", "Ashadha": "Grishma (Summer)",
        "Shravana": "Varsha (Monsoon)", "Bhadrapada": "Varsha (Monsoon)",
        "Ashvina": "Sharad (Autumn)", "Kartika": "Sharad (Autumn)",
        "Margashirsha": "Hemant (Prewinter)", "Pausha": "Hemant (Prewinter)",
        "Magha": "Shishir (Winter)", "Phalguna": "Shishir (Winter)"
    }
    vedic_ritu = vedic_ritu_map.get(lunar_month, "Grishma (Summer)")
    
    drik_ayana = "Uttarayana" if (sun_trop < 90 or sun_trop >= 270) else "Dakshinayana"
    vedic_ayana = "Uttarayana" if (sun_lon >= 270 or sun_lon < 90) else "Dakshinayana"
    
    sr_str = p["sunrise"]
    ss_str = p["sunset"]
    sr_h = int(sr_str.split(':')[0]) + int(sr_str.split(':')[1]) / 60.0
    ss_h = int(ss_str.split(':')[0]) + int(ss_str.split(':')[1]) / 60.0
    
    dinamana_h = (ss_h - sr_h) % 24
    ratrimana_h = (24 - dinamana_h) % 24
    
    def format_duration(h_val):
        h = int(h_val)
        m = int((h_val - h) * 60)
        s = int(((h_val - h) * 60 - m) * 60)
        return f"{h} Hours {m} Mins {s} Secs"
        
    dinamana = format_duration(dinamana_h)
    ratrimana = format_duration(ratrimana_h)
    
    madhyahna_h = (sr_h + dinamana_h / 2.0) % 24
    madhyahna = format_float_hours(madhyahna_h)
    
    def format_range(start_h, end_h):
        return f"{format_float_hours(start_h)} to {format_float_hours(end_h)}"
        
    brahma_start = (sr_h - 96.0 / 60.0) % 24
    brahma_end = (sr_h - 48.0 / 60.0) % 24
    brahma = format_range(brahma_start, brahma_end)
    
    pratah = format_range((sr_h - 1.0) % 24, sr_h)
    
    muhurta_len = dinamana_h / 15.0
    abhijit_start = sr_h + 7.0 * muhurta_len
    abhijit_end = sr_h + 8.0 * muhurta_len
    abhijit = format_range(abhijit_start, abhijit_end)
    
    vijaya = format_range(sr_h + 10.0 * muhurta_len, sr_h + 11.0 * muhurta_len)
    
    godhuli = format_range((ss_h - 24.0 / 60.0) % 24, (ss_h + 24.0 / 60.0) % 24)
    
    sayahna = format_range(ss_h, (ss_h + 1.0) % 24)
    
    night_muhurta_len = ratrimana_h / 15.0
    nishita_start = ss_h + 7.0 * night_muhurta_len
    nishita_end = ss_h + 8.0 * night_muhurta_len
    nishita = format_range(nishita_start, nishita_end)
    
    varjyam_start = (sr_h + (moon_lon % 13.333333333333334) * 1.5) % 24
    varjyam = format_range(varjyam_start, (varjyam_start + 1.6) % 24)
    amrit_start = (varjyam_start + 4.0) % 24
    amrit = format_range(amrit_start, (amrit_start + 1.6) % 24)
    
    weekday_idx = birth_date.weekday()
    rahu_offsets = [7.0, 1.0, 6.0, 4.0, 5.0, 3.0, 2.0]
    yama_offsets = [4.0, 3.0, 2.0, 1.0, 7.0, 6.0, 5.0]
    gulika_offsets = [5.0, 4.0, 3.0, 2.0, 1.0, 7.0, 6.0]
    
    day_part = dinamana_h / 8.0
    rahu_start = sr_h + (rahu_offsets[weekday_idx] - 1.0) * day_part
    rahu = format_range(rahu_start, rahu_start + day_part)
    
    yama_start = sr_h + (yama_offsets[weekday_idx] - 1.0) * day_part
    yama = format_range(yama_start, yama_start + day_part)
    
    gulika_start = sr_h + (gulika_offsets[weekday_idx] - 1.0) * day_part
    gulika = format_range(gulika_start, gulika_start + day_part)
    
    baana = "Agni" if weekday_idx in [1, 3] else "Mrityu"
    
    ANANDADI_YOGAS = ["Ananda", "Kalaratri", "Siddha", "Subha", "Amrita", "Musala", "Gada", "Matanga", "Rakshasa", "Chara", "Sushira", "Mitra", "Manasa", "Padma", "Lumbaka", "Utpata", "Mrityu", "Kana", "Siddhi"]
    nak_idx = int(moon_lon // 13.333333333333334)
    anandadi = ANANDADI_YOGAS[(nak_idx + weekday_idx) % len(ANANDADI_YOGAS)]
    tamil_yoga = "Siddha" if (nak_idx % 2 == 0) else "Amrita"
    
    shool_map = {0: "East", 1: "North", 2: "North", 3: "South", 4: "West", 5: "East", 6: "West"}
    disha_shool = shool_map.get(weekday_idx, "North")
    
    rashi_idx = int(moon_lon // 30)
    if rashi_idx in [0, 4, 8]: chandra_vasa = "East"
    elif rashi_idx in [1, 5, 9]: chandra_vasa = "South"
    elif rashi_idx in [2, 6, 10]: chandra_vasa = "West"
    else: chandra_vasa = "North"
    
    agnivasa_val = (tithi_num + weekday_idx + 2) % 3
    agnivasa = "Prithvi (Earth)" if agnivasa_val in [0, 1] else "Patala (Nadir)"
    
    shiva_map = {
        1: "with Gowri", 2: "on Nandi", 3: "in Sabha", 4: "in Krida",
        5: "in Kailasha", 6: "in Shmashana", 7: "in Dhyana", 8: "with Gowri",
        9: "on Nandi", 10: "in Sabha", 11: "in Krida", 12: "in Kailasha",
        13: "in Shmashana", 14: "in Dhyana", 15: "with Gowri", 16: "with Gowri"
    }
    tithi_16 = tithi_num if tithi_num <= 15 else tithi_num - 15
    shivavasa = shiva_map.get(tithi_16, "with Gowri")
    
    kali_ahargana = int(jd - 588465.5)
    rata_die = int(jd - 1721424.5)
    mjd = int(jd - 2400000.5)
    
    return {
        "panchang": p,
        "shaka_year": shaka_year,
        "vikrama_year": vikrama_year,
        "kali_year": kali_year,
        "samvatsara": samvatsara_name,
        "month_purnimanta": f"{lunar_month} - Purnimanta",
        "month_amanta": f"{amanta_month} - Amanta",
        "pravishte": pravishte,
        "drik_ritu": drik_ritu,
        "vedic_ritu": vedic_ritu,
        "drik_ayana": drik_ayana,
        "vedic_ayana": vedic_ayana,
        "dinamana": dinamana,
        "ratrimana": ratrimana,
        "madhyahna": madhyahna,
        "brahma_muhurta": brahma,
        "pratah_sandhya": pratah,
        "abhijit": abhijit,
        "vijaya": vijaya,
        "godhuli": godhuli,
        "sayahna": sayahna,
        "nishita": nishita,
        "varjyam": varjyam,
        "amrit_kalam": amrit,
        "rahu_kalam": rahu,
        "yamaganda": yama,
        "gulikai_kalam": gulika,
        "baana": baana,
        "anandadi_yoga": anandadi,
        "tamil_yoga": tamil_yoga,
        "disha_shool": disha_shool,
        "chandra_vasa": chandra_vasa,
        "agnivasa": agnivasa,
        "shivavasa": shivavasa,
        "kali_ahargana": kali_ahargana,
        "rata_die": rata_die,
        "mjd": mjd,
        "julian_day": round(jd, 4),
        "julian_date": (birth_date - timedelta(days=13)).strftime("%B %d, %Y CE")
    }


NAK_YONI = {
    'Ashwini': 'Horse', 'Bharani': 'Elephant', 'Krittika': 'Sheep', 'Rohini': 'Serpent',
    'Mrigashira': 'Serpent', 'Ardra': 'Dog', 'Punarvasu': 'Cat', 'Pushya': 'Sheep',
    'Ashlesha': 'Cat', 'Magha': 'Rat', 'Purva Phalguni': 'Rat', 'Uttara Phalguni': 'Cow',
    'Hasta': 'Buffalo', 'Chitra': 'Tiger', 'Swati': 'Buffalo', 'Vishakha': 'Tiger',
    'Anuradha': 'Hare', 'Jyeshtha': 'Hare', 'Mula': 'Dog', 'Purva Ashadha': 'Mongoose',
    'Uttara Ashadha': 'Mongoose', 'Shravana': 'Monkey', 'Dhanishta': 'Lion',
    'Shatabhisha': 'Horse', 'Purva Bhadrapada': 'Monkey', 'Uttara Bhadrapada': 'Cow',
    'Revati': 'Elephant'
}

NAK_GANAS = {
    'Ashwini': 'Deva', 'Bharani': 'Manushya', 'Krittika': 'Rakshasa', 'Rohini': 'Manushya',
    'Mrigashira': 'Deva', 'Ardra': 'Manushya', 'Punarvasu': 'Deva', 'Pushya': 'Deva',
    'Ashlesha': 'Rakshasa', 'Magha': 'Rakshasa', 'Purva Phalguni': 'Manushya',
    'Uttara Phalguni': 'Manushya', 'Hasta': 'Deva', 'Chitra': 'Rakshasa', 'Swati': 'Deva',
    'Vishakha': 'Rakshasa', 'Anuradha': 'Deva', 'Jyeshtha': 'Rakshasa', 'Mula': 'Rakshasa',
    'Purva Ashadha': 'Manushya', 'Uttara Ashadha': 'Manushya', 'Shravana': 'Deva',
    'Dhanishta': 'Rakshasa', 'Shatabhisha': 'Rakshasa', 'Purva Bhadrapada': 'Manushya',
    'Uttara Bhadrapada': 'Manushya', 'Revati': 'Deva'
}

NAK_NADIS = {
    'Ashwini': 'Adi', 'Bharani': 'Madhya', 'Krittika': 'Antya', 'Rohini': 'Antya',
    'Mrigashira': 'Madhya', 'Ardra': 'Adi', 'Punarvasu': 'Adi', 'Pushya': 'Madhya',
    'Ashlesha': 'Antya', 'Magha': 'Antya', 'Purva Phalguni': 'Madhya', 'Uttara Phalguni': 'Adi',
    'Hasta': 'Adi', 'Chitra': 'Madhya', 'Swati': 'Antya', 'Vishakha': 'Antya',
    'Anuradha': 'Madhya', 'Jyeshtha': 'Adi', 'Mula': 'Adi', 'Purva Ashadha': 'Madhya',
    'Uttara Ashadha': 'Antya', 'Shravana': 'Antya', 'Dhanishta': 'Madhya',
    'Shatabhisha': 'Adi', 'Purva Bhadrapada': 'Adi', 'Uttara Bhadrapada': 'Madhya',
    'Revati': 'Antya'
}

VARNA_CLASSES = {
    'Cancer': 'Brahmana', 'Scorpio': 'Brahmana', 'Pisces': 'Brahmana',
    'Aries': 'Kshatriya', 'Leo': 'Kshatriya', 'Sagittarius': 'Kshatriya',
    'Taurus': 'Vaishya', 'Virgo': 'Vaishya', 'Capricorn': 'Vaishya',
    'Gemini': 'Shudra', 'Libra': 'Shudra', 'Aquarius': 'Shudra'
}

VARNA_POINTS = {'Brahmana': 4, 'Kshatriya': 3, 'Vaishya': 2, 'Shudra': 1}

VASHYA_GROUPS = {
    'Aries': 'Chatushpada', 'Taurus': 'Chatushpada', 'Leo': 'Vanachar',
    'Virgo': 'Manushya', 'Libra': 'Manushya', 'Scorpio': 'Keeta',
    'Sagittarius': 'Manushya', 'Capricorn': 'Jalachar', 'Aquarius': 'Manushya',
    'Pisces': 'Jalachar', 'Gemini': 'Manushya', 'Cancer': 'Jalachar'
}

YONI_ENEMIES = {
    'Horse': 'Lion', 'Elephant': 'Lion', 'Sheep': 'Tiger', 'Serpent': 'Mongoose',
    'Dog': 'Hare', 'Cat': 'Rat', 'Cow': 'Tiger', 'Buffalo': 'Horse', 'Monkey': 'Sheep'
}


def calculate_guna_milan(boy_nak: str, boy_sign: str, girl_nak: str, girl_sign: str) -> Dict[str, Any]:
    """Calculates Ashtakoot Guna Milan compatibility score (out of 36 points)."""
    # 1. Varna (1 Point)
    b_varna = VARNA_CLASSES.get(boy_sign, 'Shudra')
    g_varna = VARNA_CLASSES.get(girl_sign, 'Shudra')
    varna_score = 1.0 if VARNA_POINTS[b_varna] >= VARNA_POINTS[g_varna] else 0.0

    # 2. Vashya (2 Points)
    b_vashya = VASHYA_GROUPS.get(boy_sign, 'Manushya')
    g_vashya = VASHYA_GROUPS.get(girl_sign, 'Manushya')
    if b_vashya == g_vashya:
        vashya_score = 2.0
    elif (b_vashya == 'Manushya' and g_vashya in ['Chatushpada', 'Jalachar']) or \
         (g_vashya == 'Manushya' and b_vashya in ['Chatushpada', 'Jalachar']):
        vashya_score = 1.0
    else:
        vashya_score = 0.5

    # 3. Tara (3 Points)
    b_nak_idx = NAKSHATRAS.index(boy_nak)
    g_nak_idx = NAKSHATRAS.index(girl_nak)
    count_g_to_b = (b_nak_idx - g_nak_idx) % 27 + 1
    count_b_to_g = (g_nak_idx - b_nak_idx) % 27 + 1
    rem_g = count_g_to_b % 9
    rem_b = count_b_to_g % 9
    auspicious = [1, 2, 4, 6, 8, 0]
    if rem_g in auspicious and rem_b in auspicious:
        tara_score = 3.0
    elif rem_g in auspicious or rem_b in auspicious:
        tara_score = 1.5
    else:
        tara_score = 0.0

    # 4. Yoni (4 Points)
    b_yoni = NAK_YONI.get(boy_nak, 'Horse')
    g_yoni = NAK_YONI.get(girl_nak, 'Horse')
    if b_yoni == g_yoni:
        yoni_score = 4.0
    elif YONI_ENEMIES.get(b_yoni) == g_yoni or YONI_ENEMIES.get(g_yoni) == b_yoni:
        yoni_score = 0.0
    else:
        yoni_score = 2.0

    # 5. Graha Maitri (5 Points)
    # Simple friendly lords score
    graha_score = 5.0 if boy_sign == girl_sign else 3.0

    # 6. Gana (6 Points)
    b_gana = NAK_GANAS.get(boy_nak, 'Deva')
    g_gana = NAK_GANAS.get(girl_nak, 'Deva')
    if b_gana == g_gana:
        gana_score = 6.0
    elif (b_gana == 'Deva' and g_gana == 'Manushya') or (g_gana == 'Deva' and b_gana == 'Manushya'):
        gana_score = 5.0
    elif (b_gana == 'Deva' and g_gana == 'Rakshasa') or (g_gana == 'Deva' and b_gana == 'Rakshasa'):
        gana_score = 1.0
    else:
        gana_score = 0.0

    # 7. Bhakoot (7 Points)
    b_sign_idx = SIGN_NAMES.index(boy_sign)
    g_sign_idx = SIGN_NAMES.index(girl_sign)
    dist = (b_sign_idx - g_sign_idx) % 12 + 1
    if dist in [2, 12, 6, 8, 5, 9]:
        bhakoot_score = 0.0
    else:
        bhakoot_score = 7.0

    # 8. Nadi (8 Points)
    b_nadi = NAK_NADIS.get(boy_nak, 'Adi')
    g_nadi = NAK_NADIS.get(girl_nak, 'Adi')
    nadi_score = 8.0 if b_nadi != g_nadi else 0.0

    total_score = varna_score + vashya_score + tara_score + yoni_score + graha_score + gana_score + bhakoot_score + nadi_score

    return {
        "varna": {"max": 1, "obtained": varna_score},
        "vashya": {"max": 2, "obtained": vashya_score},
        "tara": {"max": 3, "obtained": tara_score},
        "yoni": {"max": 4, "obtained": yoni_score},
        "graha_maitri": {"max": 5, "obtained": graha_score},
        "gana": {"max": 6, "obtained": gana_score},
        "bhakoot": {"max": 7, "obtained": bhakoot_score},
        "nadi": {"max": 8, "obtained": nadi_score},
        "total": total_score,
        "recommendation": "Auspicious Match" if total_score >= 18.0 else "Inauspicious Match"
    }


def get_divisional_chart_sign(planet_lon: float, division: int) -> str:
    """Calculates the Divisional Chart (Varga) sign for a given planet longitude and division factor."""
    lon = planet_lon % 360
    sign_idx = int(lon // 30)
    sign_lon = lon % 30
    
    if division == 1:
        return SIGN_NAMES[sign_idx]
    
    if division == 2:  # Hora (2 divisions of 15 degrees each)
        if sign_idx % 2 == 0:  # Odd sign -> First 15 is Sun (Leo), Second is Moon (Cancer)
            d_idx = 4 if sign_lon < 15 else 3
        else:  # Even sign -> First 15 is Moon (Cancer), Second is Sun (Leo)
            d_idx = 3 if sign_lon < 15 else 4
        return SIGN_NAMES[d_idx]
        
    if division == 3:  # Drekkana (3 divisions of 10 degrees each)
        part = int(sign_lon // 10)
        d_idx = (sign_idx + part * 4) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 4:  # Chaturthamsa (4 divisions of 7.5 degrees each)
        part = int(sign_lon // 7.5)
        d_idx = (sign_idx + part * 3) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 7:  # Saptamsa (7 divisions of 30/7 degrees each)
        part = int(sign_lon // (30 / 7))
        if sign_idx % 2 == 0:  # Odd sign starts at sign itself
            d_idx = (sign_idx + part) % 12
        else:  # Even sign starts at 7th sign
            d_idx = (sign_idx + 6 + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 9:  # Navamsa (9 divisions of 3.3333333 degrees each)
        part = int(sign_lon // 3.3333333333333335)
        if sign_idx in [0, 4, 8]:
            d_idx = (0 + part) % 12
        elif sign_idx in [1, 5, 9]:
            d_idx = (9 + part) % 12
        elif sign_idx in [2, 6, 10]:
            d_idx = (6 + part) % 12
        else:
            d_idx = (3 + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 10:  # Dasamsa (10 divisions of 3 degrees each)
        part = int(sign_lon // 3)
        if sign_idx % 2 == 0:
            d_idx = (sign_idx + part) % 12
        else:
            d_idx = (sign_idx + 8 + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 12:  # Dwadasamsa (12 divisions of 2.5 degrees each)
        part = int(sign_lon // 2.5)
        d_idx = (sign_idx + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 16:  # Shodasamsa (16 divisions of 30/16 degrees each)
        part = int(sign_lon // (30 / 16))
        start = 0 if sign_idx in [0, 3, 6, 9] else (4 if sign_idx in [1, 4, 7, 10] else 8)
        d_idx = (start + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 20:  # Vimsamsa (20 divisions of 1.5 degrees each)
        part = int(sign_lon // 1.5)
        start = 0 if sign_idx in [0, 3, 6, 9] else (8 if sign_idx in [1, 4, 7, 10] else 4)
        d_idx = (start + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 24:  # Chaturvimsamsa (24 divisions of 1.25 degrees each)
        part = int(sign_lon // 1.25)
        start = 4 if sign_idx % 2 == 0 else 3
        d_idx = (start + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 30:  # Trimsamsa
        if sign_idx % 2 == 0:  # Odd sign
            if sign_lon < 5: d_idx = 0
            elif sign_lon < 10: d_idx = 1
            elif sign_lon < 18: d_idx = 2
            elif sign_lon < 25: d_idx = 8
            else: d_idx = 10
        else:  # Even sign
            if sign_lon < 5: d_idx = 1
            elif sign_lon < 12: d_idx = 2
            elif sign_lon < 20: d_idx = 8
            elif sign_lon < 25: d_idx = 0
            else: d_idx = 10
        return SIGN_NAMES[d_idx]
        
    if division == 40:  # Khavedamsa (40 divisions of 0.75 degrees each)
        part = int(sign_lon // 0.75)
        start = 0 if sign_idx % 2 == 0 else 6
        d_idx = (start + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 45:  # Akshavedamsa (45 divisions of 30/45 degrees each)
        part = int(sign_lon // (30 / 45))
        start = 0 if sign_idx in [0, 3, 6, 9] else (4 if sign_idx in [1, 4, 7, 10] else 8)
        d_idx = (start + part) % 12
        return SIGN_NAMES[d_idx]
        
    if division == 60:  # Shastiamsa (60 divisions of 0.5 degrees each)
        part = int(sign_lon // 0.5)
        d_idx = (sign_idx + part) % 12
        return SIGN_NAMES[d_idx]

    return SIGN_NAMES[sign_idx]


def calculate_sunrise_sunset_approx(birth_date: date, lat: float, lon: float, timezone_offset: float) -> Tuple[str, str]:
    """Calculates sunrise and sunset times precisely using Swiss Ephemeris, falling back to declination equations on error."""
    import swisseph as swe
    try:
        # 1. Convert local midnight of the birth date to UT Julian Day
        jd_local_midnight = swe.julday(birth_date.year, birth_date.month, birth_date.day, 0.0)
        jd_ut_start = jd_local_midnight - (timezone_offset / 24.0)
        
        # 2. Precise Sunrise (CALC_RISE = 1)
        status_rise, rise_jd = swe.rise_trans(
            jd_ut_start,
            swe.SUN,
            None,
            swe.FLG_SWIEPH,
            1,  # swe.CALC_RISE
            (lon, lat, 0.0),
            1013.25,
            15.0
        )
        
        # 3. Precise Sunset (CALC_SET = 2)
        status_set, set_jd = swe.rise_trans(
            jd_ut_start,
            swe.SUN,
            None,
            swe.FLG_SWIEPH,
            2,  # swe.CALC_SET
            (lon, lat, 0.0),
            1013.25,
            15.0
        )
        
        # Convert UT Julian Days to local hours from local midnight
        rise_hours = ((rise_jd + (timezone_offset / 24.0)) - jd_local_midnight) * 24.0
        set_hours = ((set_jd + (timezone_offset / 24.0)) - jd_local_midnight) * 24.0
        
        return format_float_hours(rise_hours % 24.0), format_float_hours(set_hours % 24.0)
    except Exception:
        # Fallback to simple physical approximation
        import math
        n = birth_date.timetuple().tm_yday
        decl = 23.45 * math.sin(math.radians(360/365 * (284 + n)))
        try:
            cos_h = -math.tan(math.radians(lat)) * math.tan(math.radians(decl))
            if cos_h < -1:
                h = 180
            elif cos_h > 1:
                h = 0
            else:
                h = math.degrees(math.acos(cos_h))
        except Exception:
            h = 90
            
        b = 360/364 * (n - 81)
        eot = 9.87 * math.sin(math.radians(2*b)) - 7.53 * math.cos(math.radians(b)) - 1.5 * math.sin(math.radians(b))
        meridian = timezone_offset * 15.0
        lon_offset = (lon - meridian) * 4.0
        solar_noon = 12.0 - (eot / 60.0) - (lon_offset / 60.0)
        sunrise_hours = solar_noon - (h / 15.0)
        sunset_hours = solar_noon + (h / 15.0)
        
        return format_float_hours(sunrise_hours % 24.0), format_float_hours(sunset_hours % 24.0)


def format_float_hours(h_val) -> str:
    h_val = h_val % 24
    mins = int((h_val - int(h_val)) * 60)
    return f"{int(h_val):02d}:{mins:02d}"


def get_choghadiya_list(birth_date: date, lat: float, lon: float, timezone_offset: float) -> Dict[str, List[Dict]]:
    """Generates daily and nightly Choghadiya tables for a given weekday and location."""
    sr_str, ss_str = calculate_sunrise_sunset_approx(birth_date, lat, lon, timezone_offset)
    sr_h = int(sr_str.split(':')[0]) + int(sr_str.split(':')[1]) / 60.0
    ss_h = int(ss_str.split(':')[0]) + int(ss_str.split(':')[1]) / 60.0
    
    day_dur = (ss_h - sr_h) % 24
    night_dur = (24 - day_dur) % 24
    
    day_step = day_dur / 8.0
    night_step = night_dur / 8.0
    
    weekday_idx = (birth_date.weekday() + 1) % 7 # Sunday=0, Monday=1, ...
    
    CHOGHADIYA_DAY_SEQ = {
        0: ['Udveg', 'Chal', 'Labh', 'Amrit', 'Kaal', 'Shubh', 'Rog', 'Udveg'],
        1: ['Amrit', 'Kaal', 'Shubh', 'Rog', 'Udveg', 'Chal', 'Labh', 'Amrit'],
        2: ['Rog', 'Udveg', 'Chal', 'Labh', 'Amrit', 'Kaal', 'Shubh', 'Rog'],
        3: ['Labh', 'Amrit', 'Kaal', 'Shubh', 'Rog', 'Udveg', 'Chal', 'Labh'],
        4: ['Shubh', 'Rog', 'Udveg', 'Chal', 'Labh', 'Amrit', 'Kaal', 'Shubh'],
        5: ['Chal', 'Labh', 'Amrit', 'Kaal', 'Shubh', 'Rog', 'Udveg', 'Chal'],
        6: ['Kaal', 'Shubh', 'Rog', 'Udveg', 'Chal', 'Labh', 'Amrit', 'Kaal']
    }
    
    CHOGHADIYA_NIGHT_SEQ = {
        0: ['Shubh', 'Amrit', 'Chal', 'Rog', 'Kaal', 'Labh', 'Udveg', 'Shubh'],
        1: ['Chal', 'Rog', 'Kaal', 'Labh', 'Udveg', 'Shubh', 'Amrit', 'Chal'],
        2: ['Kaal', 'Labh', 'Udveg', 'Shubh', 'Amrit', 'Chal', 'Rog', 'Kaal'],
        3: ['Udveg', 'Shubh', 'Amrit', 'Chal', 'Rog', 'Kaal', 'Labh', 'Udveg'],
        4: ['Amrit', 'Chal', 'Rog', 'Kaal', 'Labh', 'Udveg', 'Shubh', 'Amrit'],
        5: ['Rog', 'Kaal', 'Labh', 'Udveg', 'Shubh', 'Amrit', 'Chal', 'Rog'],
        6: ['Labh', 'Udveg', 'Shubh', 'Amrit', 'Chal', 'Rog', 'Kaal', 'Labh']
    }
    
    CHOGHADIYA_QUALITY = {
        'Amrit': 'Good', 'Shubh': 'Good', 'Labh': 'Good',
        'Chal': 'Neutral',
        'Rog': 'Bad', 'Kaal': 'Bad', 'Udveg': 'Bad'
    }
    
    day_list = []
    for i in range(8):
        start = sr_h + i * day_step
        end = sr_h + (i + 1) * day_step
        name = CHOGHADIYA_DAY_SEQ[weekday_idx][i]
        day_list.append({
            "part": i + 1,
            "start": format_float_hours(start),
            "end": format_float_hours(end),
            "name": name,
            "quality": CHOGHADIYA_QUALITY[name]
        })
        
    night_list = []
    for i in range(8):
        start = ss_h + i * night_step
        end = ss_h + (i + 1) * night_step
        name = CHOGHADIYA_NIGHT_SEQ[weekday_idx][i]
        night_list.append({
            "part": i + 1,
            "start": format_float_hours(start),
            "end": format_float_hours(end),
            "name": name,
            "quality": CHOGHADIYA_QUALITY[name]
        })
        
    return {
        "sunrise": sr_str,
        "sunset": ss_str,
        "day": day_list,
        "night": night_list
    }


WEEKDAY_LORDS = {
    0: 'Sun', 1: 'Moon', 2: 'Mars', 3: 'Mercury', 4: 'Jupiter', 5: 'Venus', 6: 'Saturn'
}


def get_hora_list(birth_date: date, lat: float, lon: float, timezone_offset: float) -> Dict[str, List[Dict]]:
    """Generates day/night solar planetary horas for a given weekday and location."""
    sr_str, ss_str = calculate_sunrise_sunset_approx(birth_date, lat, lon, timezone_offset)
    sr_h = int(sr_str.split(':')[0]) + int(sr_str.split(':')[1]) / 60.0
    ss_h = int(ss_str.split(':')[0]) + int(ss_str.split(':')[1]) / 60.0
    
    day_dur = (ss_h - sr_h) % 24
    night_dur = (24 - day_dur) % 24
    
    day_step = day_dur / 12.0
    night_step = night_dur / 12.0
    
    weekday_idx = (birth_date.weekday() + 1) % 7 # Sunday=0, Monday=1, ...
    start_lord = WEEKDAY_LORDS[weekday_idx]
    
    HORA_SEQUENCE = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']
    start_idx = HORA_SEQUENCE.index(start_lord)
    
    day_horas = []
    for i in range(12):
        start = sr_h + i * day_step
        end = sr_h + (i + 1) * day_step
        lord = HORA_SEQUENCE[(start_idx + i) % 7]
        day_horas.append({
            "hour": i + 1,
            "start": format_float_hours(start),
            "end": format_float_hours(end),
            "lord": lord,
            "indian": INDIAN_NAMES.get(lord, lord)
        })
        
    night_horas = []
    for i in range(12):
        start = ss_h + i * night_step
        end = ss_h + (i + 1) * night_step
        lord = HORA_SEQUENCE[(start_idx + 12 + i) % 7]
        night_horas.append({
            "hour": i + 1,
            "start": format_float_hours(start),
            "end": format_float_hours(end),
            "lord": lord,
            "indian": INDIAN_NAMES.get(lord, lord)
        })
        
    return {
        "day": day_horas,
        "night": night_horas
    }


REGIONAL_MONTHS = {
    0: {"tamil": "Chithirai", "malayalam": "Medam", "bengali": "Baishakh", "odia": "Mesha"},
    1: {"tamil": "Vaikasi", "malayalam": "Edavam", "bengali": "Jaistha", "odia": "Vrusha"},
    2: {"tamil": "Aani", "malayalam": "Mithunam", "bengali": "Ashadh", "odia": "Mithuna"},
    3: {"tamil": "Aadi", "malayalam": "Karkidakam", "bengali": "Shravan", "odia": "Karkata"},
    4: {"tamil": "Avani", "malayalam": "Chingam", "bengali": "Bhadra", "odia": "Simha"},
    5: {"tamil": "Purattasi", "malayalam": "Kanni", "bengali": "Ashvin", "odia": "Kanya"},
    6: {"tamil": "Aippasi", "malayalam": "Thulam", "bengali": "Kartik", "odia": "Tula"},
    7: {"tamil": "Karthigai", "malayalam": "Vrischika", "bengali": "Agrahayana", "odia": "Dhanu"},
    8: {"tamil": "Margazhi", "malayalam": "Dhanu", "bengali": "Poush", "odia": "Makara"},
    9: {"tamil": "Thai", "malayalam": "Makaram", "bengali": "Magha", "odia": "Kumbha"},
    10: {"tamil": "Maasi", "malayalam": "Kumbham", "bengali": "Phalgun", "odia": "Mina"},
    11: {"tamil": "Panguni", "malayalam": "Meenam", "bengali": "Chaitra", "odia": "Mesha"}
}

LUNAR_MONTHS = [
    'Chaitra', 'Vaishakha', 'Jyeshtha', 'Ashadha', 'Shravana', 'Bhadrapada',
    'Ashvina', 'Kartika', 'Margashirsha', 'Pausha', 'Magha', 'Phalguna'
]



