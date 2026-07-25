# -*- coding: utf-8 -*-
"""
Astronomy Engine: Precision Astronomical Formulae Wrapper utilizing Swiss Ephemeris or pure math fallback.
"""
from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
import math
from typing import Dict, Any, Tuple, Optional

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

# Map of Ayanamsa Names to Swiss Ephemeris Constants
AYANAMSA_MAP = {
    "Lahiri": getattr(swe, 'SIDM_LAHIRI', 1) if HAS_SWISSEPH else 1,
    "Chitrapaksha": getattr(swe, 'SIDM_LAHIRI', 1) if HAS_SWISSEPH else 1,
    "Raman": getattr(swe, 'SIDM_RAMAN', 3) if HAS_SWISSEPH else 3,
    "KP": getattr(swe, 'SIDM_KRISHNAMURTI', 5) if HAS_SWISSEPH else 5,
    "Krishnamurti": getattr(swe, 'SIDM_KRISHNAMURTI', 5) if HAS_SWISSEPH else 5,
    "Yukteswar": getattr(swe, 'SIDM_YUKTESHWAR', 7) if HAS_SWISSEPH else 7,
    "Sri Yukteswar": getattr(swe, 'SIDM_YUKTESHWAR', 7) if HAS_SWISSEPH else 7,
    "Fagan Bradley": getattr(swe, 'SIDM_FAGAN_BRADLEY', 0) if HAS_SWISSEPH else 0,
    "Fagan-Bradley": getattr(swe, 'SIDM_FAGAN_BRADLEY', 0) if HAS_SWISSEPH else 0,
    "De Luce": getattr(swe, 'SIDM_DELUCE', 2) if HAS_SWISSEPH else 2,
    "True Chitrapaksha": getattr(swe, 'SIDM_TRUE_CITRA', 27) if HAS_SWISSEPH else 27,
    "TrueChitra": getattr(swe, 'SIDM_TRUE_CITRA', 27) if HAS_SWISSEPH else 27,
    "Pushya Paksha": getattr(swe, 'SIDM_PUSHYA', 29) if HAS_SWISSEPH else 29,
    "SS Citra": getattr(swe, 'SIDM_SURYA_CITRA', 30) if HAS_SWISSEPH else 30,
    "Surya Siddhanta": getattr(swe, 'SIDM_SURYASIDDHANTA', 21) if HAS_SWISSEPH else 21,
    "Aryabhata": getattr(swe, 'SIDM_ARYABHATA', 23) if HAS_SWISSEPH else 23,
    "User-defined": -99,
    "Tropical": -1
}

HOUSE_SYSTEM_MAP = {
    "Whole Sign": b'W',
    "Equal": b'A',
    "Sripati": b'E',
    "Porphyry": b'P',
    "Koch": b'K',
    "Placidus": b'P',
    "Regiomontanus": b'R',
    "Campanus": b'C',
    "Topocentric": b'T',
    "Morinus": b'M',
    "Alcabitius": b'B',
    "Meridian": b'X',
    "Vehlow Equal": b'V'
}


@dataclass
class AstronomicalData:
    julian_day_ut: float
    julian_day_tt: float
    delta_t: float
    true_obliquity: float
    mean_obliquity: float
    nutation_lon: float
    nutation_obl: float
    sidereal_time_ut: float
    sidereal_time_local: float
    ayanamsa_name: str
    ayanamsa_val: float
    sunrise_ut: Optional[float] = None
    sunset_ut: Optional[float] = None
    moonrise_ut: Optional[float] = None
    moonset_ut: Optional[float] = None

class AstronomyEngine:
    """Core Astronomical Calculations using Swiss Ephemeris with pure math fallback."""
    
    @staticmethod
    def compute_julian_day(year: int, month: int, day: int, hour: float = 0.0) -> float:
        """Calculate Julian Day Number in Universal Time (UT)."""
        if HAS_SWISSEPH:
            return swe.julday(year, month, day, hour, swe.GREG_CAL)
        else:
            y, m = year, month
            if m <= 2:
                y -= 1
                m += 12
            A = math.floor(y / 100)
            B = 2 - A + math.floor(A / 4)
            return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + day + B - 1524.5 + (hour / 24.0)

    @staticmethod
    def get_ayanamsa_value(jd_ut: float, ayanamsa_name: str = "Lahiri", custom_offset: float = 0.0) -> float:
        """Compute Ayanamsa value in degrees for a given Julian Day and Ayanamsa system."""
        if ayanamsa_name == "Tropical":
            return 0.0
        
        if HAS_SWISSEPH:
            mode = AYANAMSA_MAP.get(ayanamsa_name, swe.SIDM_LAHIRI)
            swe.set_sid_mode(mode)
            base_ay = swe.get_ayanamsa_ut(jd_ut)
            return base_ay + custom_offset
        else:
            # Mathematical approximation: Lahiri ayanamsa at J2000.0 is 23.85°, precessing ~50.29"/yr
            T = (jd_ut - 2451545.0) / 36525.0
            lahiri_ay = 23.85 + 1.396 * T
            if ayanamsa_name == "Raman":
                return lahiri_ay - 1.4 + custom_offset
            elif ayanamsa_name in ["KP", "Krishnamurti"]:
                return lahiri_ay - 0.1 + custom_offset
            elif ayanamsa_name in ["Fagan", "Fagan-Bradley"]:
                return lahiri_ay + 0.9 + custom_offset
            return lahiri_ay + custom_offset

    @classmethod
    def calculate_astronomy_data(
        cls,
        dt_ut: datetime,
        lat: float,
        lon: float,
        ayanamsa_name: str = "Lahiri",
        custom_ayanamsa_offset: float = 0.0
    ) -> AstronomicalData:
        """Compute full set of astronomical variables for birth time and location."""
        hour_frac = dt_ut.hour + dt_ut.minute / 60.0 + dt_ut.second / 3600.0 + dt_ut.microsecond / 3600000000.0
        jd_ut = cls.compute_julian_day(dt_ut.year, dt_ut.month, dt_ut.day, hour_frac)
        
        if HAS_SWISSEPH:
            delta_t_sec = swe.deltat(jd_ut)
            jd_tt = jd_ut + (delta_t_sec / 86400.0)
            ecl_nut, _ = swe.calc_ut(jd_ut, swe.ECL_NUT)
            true_obl, mean_obl, nut_lon, nut_obl = ecl_nut[0], ecl_nut[1], ecl_nut[2], ecl_nut[3]
            gst_hours = swe.sidtime(jd_ut)
        else:
            delta_t_sec = 69.18 # Approximate Delta T
            jd_tt = jd_ut + (delta_t_sec / 86400.0)
            T = (jd_ut - 2451545.0) / 36525.0
            mean_obl = 23.439291 - 0.0130042 * T
            true_obl = mean_obl
            nut_lon = 0.0048 * math.sin(math.radians(125.0 - 1934.1 * T))
            nut_obl = 0.0025 * math.cos(math.radians(125.0 - 1934.1 * T))
            gst_hours = (18.697374558 + 24.06570982441908 * (jd_ut - 2451545.0)) % 24.0

        lst_hours = (gst_hours + lon / 15.0) % 24.0
        ay_val = cls.get_ayanamsa_value(jd_ut, ayanamsa_name, custom_ayanamsa_offset)
        
        sunrise_ut = cls.get_rise_set(jd_ut, lat, lon, 0, 1) if HAS_SWISSEPH else (jd_ut - (hour_frac - 6.0)/24.0)
        sunset_ut = cls.get_rise_set(jd_ut, lat, lon, 0, 2) if HAS_SWISSEPH else (jd_ut - (hour_frac - 18.0)/24.0)
        moonrise_ut = cls.get_rise_set(jd_ut, lat, lon, 1, 1) if HAS_SWISSEPH else None
        moonset_ut = cls.get_rise_set(jd_ut, lat, lon, 1, 2) if HAS_SWISSEPH else None
        
        return AstronomicalData(
            julian_day_ut=jd_ut,
            julian_day_tt=jd_tt,
            delta_t=delta_t_sec,
            true_obliquity=true_obl,
            mean_obliquity=mean_obl,
            nutation_lon=nut_lon,
            nutation_obl=nut_obl,
            sidereal_time_ut=gst_hours,
            sidereal_time_local=lst_hours,
            ayanamsa_name=ayanamsa_name,
            ayanamsa_val=ay_val,
            sunrise_ut=sunrise_ut,
            sunset_ut=sunset_ut,
            moonrise_ut=moonrise_ut,
            moonset_ut=moonset_ut
        )

    @staticmethod
    def get_rise_set(jd_ut: float, lat: float, lon: float, body: int, flag: int) -> Optional[float]:
        """Get rise or set Julian Day for Sun/Moon."""
        if not HAS_SWISSEPH:
            return None
        try:
            geopos = (lon, lat, 0.0)
            res, ret_jd = swe.rise_trans(jd_ut, body, flag | swe.BIT_DISC_CENTER, geopos)
            if res == 0 and len(ret_jd) > 0:
                return ret_jd[0]
        except Exception:
            pass
        return None

