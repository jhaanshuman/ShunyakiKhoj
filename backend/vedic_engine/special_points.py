# -*- coding: utf-8 -*-
"""
Special Points Engine: Computes Special Lagnas, Upagrahas, Sahams, and Sensitive Points.
"""
from dataclasses import dataclass
from typing import Dict, Any, Tuple
from .planets import SIGN_NAMES, NAKSHATRAS, NAKSHATRA_LORDS, SIGN_LORDS

# Ray points for Indu Lagna
INDU_RAYS = {
    'Sun': 30, 'Moon': 16, 'Mars': 6, 'Mercury': 8,
    'Jupiter': 10, 'Venus': 12, 'Saturn': 1
}

@dataclass
class PointDetail:
    name: str
    sidereal_lon: float
    sign_name: str
    sign_lord: str
    sign_degree: float
    nakshatra_name: str
    nakshatra_lord: str
    pada: int
    house: int

class SpecialPointsEngine:
    """Calculates Special Lagnas, Upagrahas, and Sensitive Points."""
    
    @staticmethod
    def get_point_detail(name: str, sid_lon: float, asc_sign_idx: int) -> PointDetail:
        sid_lon = sid_lon % 360.0
        sign_idx = int(sid_lon // 30)
        sign_name = SIGN_NAMES[sign_idx]
        sign_lord = SIGN_LORDS[sign_name]
        sign_deg = sid_lon % 30.0
        
        nak_idx = int(sid_lon // (360.0 / 27.0))
        nak_name = NAKSHATRAS[nak_idx]
        nak_lord = NAKSHATRA_LORDS[nak_idx]
        pada = int((sid_lon % (360.0 / 27.0)) // (360.0 / 108.0)) + 1
        
        h_num = ((sign_idx - asc_sign_idx) % 12) + 1
        
        return PointDetail(
            name=name,
            sidereal_lon=sid_lon,
            sign_name=sign_name,
            sign_lord=sign_lord,
            sign_degree=sign_deg,
            nakshatra_name=nak_name,
            nakshatra_lord=nak_lord,
            pada=pada,
            house=h_num
        )

    @classmethod
    def calculate_special_points(
        cls,
        asc_sid_lon: float,
        sun_sid_lon: float,
        moon_sid_lon: float,
        rahu_sid_lon: float,
        mars_sid_lon: float,
        jupiter_sid_lon: float,
        venus_sid_lon: float,
        sunrise_jd: float,
        birth_jd: float
    ) -> Dict[str, PointDetail]:
        """Compute all special points, lagnas, and upagrahas."""
        asc_sign_idx = int((asc_sid_lon % 360.0) // 30)
        points: Dict[str, PointDetail] = {}
        
        # Time difference from sunrise in hours
        dt_hours = max((birth_jd - sunrise_jd) * 24.0, 0.0) if sunrise_jd else 0.0
        
        # 1. Special Lagnas
        # Hora Lagna: moves 1 sign (30°) per hour from Sun
        hl_lon = (sun_sid_lon + dt_hours * 30.0) % 360.0
        points['Hora Lagna'] = cls.get_point_detail('Hora Lagna', hl_lon, asc_sign_idx)
        
        # Ghati Lagna: moves 1 sign (30°) per 24 mins (0.4 hours) from Sun
        gl_lon = (sun_sid_lon + (dt_hours / 0.4) * 30.0) % 360.0
        points['Ghati Lagna'] = cls.get_point_detail('Ghati Lagna', gl_lon, asc_sign_idx)
        
        # Bhava Lagna: moves 1 sign (30°) per 2 hours from Sun
        bl_lon = (sun_sid_lon + (dt_hours / 2.0) * 30.0) % 360.0
        points['Bhava Lagna'] = cls.get_point_detail('Bhava Lagna', bl_lon, asc_sign_idx)
        
        # Indu Lagna: Sum of rays of 9th lord from Sun and 9th lord from Moon
        sun_9th_lord = SIGN_LORDS[SIGN_NAMES[(int(sun_sid_lon // 30) + 8) % 12]]
        moon_9th_lord = SIGN_LORDS[SIGN_NAMES[(int(moon_sid_lon // 30) + 8) % 12]]
        indu_rays = INDU_RAYS.get(sun_9th_lord, 1) + INDU_RAYS.get(moon_9th_lord, 1)
        indu_sign_offset = (indu_rays % 12)
        indu_lon = ((int(moon_sid_lon // 30) + indu_sign_offset) * 30.0 + (moon_sid_lon % 30.0)) % 360.0
        points['Indu Lagna'] = cls.get_point_detail('Indu Lagna', indu_lon, asc_sign_idx)
        
        # Sree Lagna: Based on Moon Nakshatra fraction added to Lagna
        moon_nak_frac = (moon_sid_lon % (360.0 / 27.0)) / (360.0 / 27.0)
        sree_lon = (asc_sid_lon + moon_nak_frac * 360.0) % 360.0
        points['Sree Lagna'] = cls.get_point_detail('Sree Lagna', sree_lon, asc_sign_idx)

        # 2. Sensitive Points
        # Bhrigu Bindu: Midpoint between Moon and Rahu
        bb_lon = ((moon_sid_lon + rahu_sid_lon) / 2.0) % 360.0
        points['Bhrigu Bindu'] = cls.get_point_detail('Bhrigu Bindu', bb_lon, asc_sign_idx)
        
        # 64th Navamsa: 210° (7 signs + 8°) from Lagna
        nav64_lon = (asc_sid_lon + 210.0) % 360.0
        points['64th Navamsa'] = cls.get_point_detail('64th Navamsa', nav64_lon, asc_sign_idx)
        
        # 22nd Drekkana: 210° from Lagna
        drek22_lon = (asc_sid_lon + 210.0) % 360.0
        points['22nd Drekkana'] = cls.get_point_detail('22nd Drekkana', drek22_lon, asc_sign_idx)

        # Beeja Sphuta (Male fertility: Sun + Venus + Jupiter)
        beeja_lon = (sun_sid_lon + venus_sid_lon + jupiter_sid_lon) % 360.0
        points['Beeja Sphuta'] = cls.get_point_detail('Beeja Sphuta', beeja_lon, asc_sign_idx)

        # Kshetra Sphuta (Female fertility: Moon + Mars + Jupiter)
        kshetra_lon = (moon_sid_lon + mars_sid_lon + jupiter_sid_lon) % 360.0
        points['Kshetra Sphuta'] = cls.get_point_detail('Kshetra Sphuta', kshetra_lon, asc_sign_idx)

        # 3. Upagrahas (Shadow Planets)
        dhuma = (sun_sid_lon + 133.333333) % 360.0
        vyatipata = (360.0 - dhuma) % 360.0
        parivesha = (vyatipata + 180.0) % 360.0
        indrachapa = (360.0 - parivesha) % 360.0
        upaketu = (indrachapa + 16.666667) % 360.0
        
        points['Dhuma'] = cls.get_point_detail('Dhuma', dhuma, asc_sign_idx)
        points['Vyatipata'] = cls.get_point_detail('Vyatipata', vyatipata, asc_sign_idx)
        points['Parivesha'] = cls.get_point_detail('Parivesha', parivesha, asc_sign_idx)
        points['Indrachapa'] = cls.get_point_detail('Indrachapa', indrachapa, asc_sign_idx)
        points['Upaketu'] = cls.get_point_detail('Upaketu', upaketu, asc_sign_idx)

        # Mandi & Gulika (proportional to sunrise time)
        mandi_lon = (sun_sid_lon + (dt_hours / 24.0) * 360.0 + 90.0) % 360.0
        gulika_lon = (sun_sid_lon + (dt_hours / 24.0) * 360.0 + 60.0) % 360.0
        points['Mandi'] = cls.get_point_detail('Mandi', mandi_lon, asc_sign_idx)
        points['Gulika'] = cls.get_point_detail('Gulika', gulika_lon, asc_sign_idx)

        return points
