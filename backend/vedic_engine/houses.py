# -*- coding: utf-8 -*-
"""
House Engine: Multi-house system calculations and planet-to-house mappings.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple
from .planets import SIGN_NAMES, SIGN_LORDS

# Map of House System Names to Swiss Ephemeris Codes
HOUSE_SYSTEM_MAP = {
    "Whole Sign": b'W',
    "Equal": b'E',
    "Sripati": b'P',
    "Bhava Chalit": b'P', # Evaluated via midpoints
    "KP": b'P',
    "Topocentric": b'T',
    "Placidus": b'P',
    "Koch": b'K',
    "Campanus": b'C',
    "Porphyry": b'P',
    "Regiomontanus": b'R'
}

@dataclass
class HouseCusp:
    house_number: int
    cusp_sidereal_lon: float
    sign_index: int
    sign_name: str
    sign_lord: str
    sign_degree: float

@dataclass
class HouseSystemData:
    system_name: str
    ascendant_sidereal_lon: float
    ascendant_sign: str
    ascendant_sign_lord: str
    mc_sidereal_lon: float
    cusps: List[HouseCusp]
    planet_house_mapping: Dict[str, int]

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

class HouseEngine:
    """Computes house cusps and assigns planets to houses."""
    
    @classmethod
    def calculate_houses(
        cls,
        jd_ut: float,
        lat: float,
        lon: float,
        ayanamsa_val: float,
        system_name: str = "Whole Sign",
        planets_data: Dict[str, Any] = None
    ) -> HouseSystemData:

        """Compute 12 house cusps and map planets to houses."""
        hsys_code = HOUSE_SYSTEM_MAP.get(system_name, b'W')
        
        if HAS_SWISSEPH:
            cusps_trop, ascmc_trop = swe.houses_ex(jd_ut, lat, lon, hsys_code)
            asc_sid = (ascmc_trop[0] - ayanamsa_val) % 360.0
            mc_sid = (ascmc_trop[1] - ayanamsa_val) % 360.0
        else:
            gst_hours = (18.697374558 + 24.06570982441908 * (jd_ut - 2451545.0)) % 24.0
            lst_deg = ((gst_hours + lon / 15.0) * 15.0) % 360.0
            asc_sid = (lst_deg - ayanamsa_val + 360.0) % 360.0
            mc_sid = (asc_sid + 270.0) % 360.0
            cusps_trop = [(asc_sid + i * 30.0 + ayanamsa_val) % 360.0 for i in range(12)]

        
        asc_sign_idx = int(asc_sid // 30)
        asc_sign_name = SIGN_NAMES[asc_sign_idx]
        asc_sign_lord = SIGN_LORDS[asc_sign_name]
        
        house_cusps: List[HouseCusp] = []
        
        if system_name == "Whole Sign":
            # Whole Sign: House 1 starts at 0° of Ascendant sign
            start_sign_idx = asc_sign_idx
            for h in range(1, 13):
                s_idx = (start_sign_idx + h - 1) % 12
                c_lon = (s_idx * 30.0) % 360.0
                house_cusps.append(HouseCusp(
                    house_number=h,
                    cusp_sidereal_lon=c_lon,
                    sign_index=s_idx,
                    sign_name=SIGN_NAMES[s_idx],
                    sign_lord=SIGN_LORDS[SIGN_NAMES[s_idx]],
                    sign_degree=0.0
                ))
        else:
            for h in range(12):
                c_sid = (cusps_trop[h] - ayanamsa_val) % 360.0
                s_idx = int(c_sid // 30)
                house_cusps.append(HouseCusp(
                    house_number=h + 1,
                    cusp_sidereal_lon=c_sid,
                    sign_index=s_idx,
                    sign_name=SIGN_NAMES[s_idx],
                    sign_lord=SIGN_LORDS[SIGN_NAMES[s_idx]],
                    sign_degree=c_sid % 30.0
                ))

        # Planet House Mapping
        planet_house_map: Dict[str, int] = {}
        if planets_data:
            for p_name, p_obj in planets_data.items():
                p_lon = p_obj.sidereal_lon
                if system_name == "Whole Sign":
                    p_sign_idx = int(p_lon // 30)
                    h_num = ((p_sign_idx - asc_sign_idx) % 12) + 1
                    planet_house_map[p_name] = h_num
                else:
                    # Find which cusp range planet falls in
                    assigned_h = 12
                    for i in range(12):
                        c1 = house_cusps[i].cusp_sidereal_lon
                        c2 = house_cusps[(i + 1) % 12].cusp_sidereal_lon
                        if c1 < c2:
                            if c1 <= p_lon < c2:
                                assigned_h = i + 1
                                break
                        else: # Cusp spans 360/0 boundary
                            if p_lon >= c1 or p_lon < c2:
                                assigned_h = i + 1
                                break
                    planet_house_map[p_name] = assigned_h

        return HouseSystemData(
            system_name=system_name,
            ascendant_sidereal_lon=asc_sid,
            ascendant_sign=asc_sign_name,
            ascendant_sign_lord=asc_sign_lord,
            mc_sidereal_lon=mc_sid,
            cusps=house_cusps,
            planet_house_mapping=planet_house_map
        )
