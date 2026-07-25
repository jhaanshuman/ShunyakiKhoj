# -*- coding: utf-8 -*-
"""
KP Engine Orchestrator v5.0.
Calculates KP Cusps, Sub-Lords, Sub-Sub-Lords, Significators, and Ruling Planets.
"""

from .cusps import calculate_kp_cusps
from .sublords import get_sublords
from .significators import calculate_kp_significators
from .ruling_planets import calculate_ruling_planets

def calculate_kp(master_obj: dict) -> dict:
    """Orchestrator for complete KP Analysis."""
    planets = master_obj.get('planets', {})
    houses_info = master_obj.get('houses', {})

    # Cusps longitudes dictionary {1..12: float}
    cusps_data = {}
    if isinstance(houses_info, dict):
        c_list = houses_info.get('house_cusps', [])
        if isinstance(c_list, list) and len(c_list) >= 12:
            for idx, c in enumerate(c_list[:12]):
                lon_val = c.get('sidereal_lon', c.get('longitude', 0.0)) if isinstance(c, dict) else float(c)
                cusps_data[idx + 1] = lon_val

    if not cusps_data:
        asc_lon = houses_info.get('ascendant_sidereal_lon', 0.0) if isinstance(houses_info, dict) else 0.0
        cusps_data = {h: (asc_lon + (h - 1) * 30.0) % 360.0 for h in range(1, 13)}

    day_lord = master_obj.get('panchanga', {}).get('vaara', 'Sun') if isinstance(master_obj.get('panchanga'), dict) else 'Sun'

    # 1. Calculate sublords for all planets
    planets_kp = {}
    for p, data in planets.items():
        lon = data.get('sidereal_lon', data.get('lon', 0.0))
        planets_kp[p] = get_sublords(lon)
        planets_kp[p]['house_occupying'] = data.get('house', 1)

    # 2. Calculate sublords for all house cusps
    house_cusps_kp = {}
    for h_num, lon in cusps_data.items():
        house_cusps_kp[h_num] = get_sublords(lon)
        house_cusps_kp[h_num]['longitude'] = round(lon, 4)

    # 3. Significators
    significators = calculate_kp_significators(planets_kp, house_cusps_kp)

    # 4. Ruling Planets
    lagna_lon = cusps_data.get(1, 0.0)
    moon_lon = planets.get('Moon', {}).get('sidereal_lon', planets.get('Moon', {}).get('lon', 0.0))

    lagna_lords = get_sublords(lagna_lon)
    moon_lords = get_sublords(moon_lon)
    ruling_planets = calculate_ruling_planets(lagna_lords, moon_lords, day_lord)

    return {
        'status': 'success',
        'cusps': house_cusps_kp,
        'planets': planets_kp,
        'significators': significators,
        'ruling_planets': ruling_planets
    }
