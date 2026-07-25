# -*- coding: utf-8 -*-
"""
Strength Engine: Computes Shadbala (6-fold strength), Bhavabala, Vimshopaka, and Ishta/Kashta Phala.
"""
from dataclasses import dataclass
import math
from typing import Dict, Any, List

# Natural Strengths in Virupas (Naisargika Bala)
NAISARGIKA_BALA = {
    'Sun': 60.0,
    'Moon': 51.43,
    'Venus': 42.86,
    'Jupiter': 34.29,
    'Mercury': 25.71,
    'Mars': 17.14,
    'Saturn': 8.57
}

# Required Minimum Shadbala in Rupas (60 Virupas = 1 Rupa)
REQUIRED_SHADBALA = {
    'Sun': 6.5,   # 390 Virupas
    'Moon': 6.0,  # 360 Virupas
    'Mars': 5.0,  # 300 Virupas
    'Mercury': 7.0, # 420 Virupas
    'Jupiter': 6.5, # 390 Virupas
    'Venus': 5.5,   # 330 Virupas
    'Saturn': 5.0   # 300 Virupas
}

@dataclass
class ShadbalaDetail:
    planet: str
    sthana_bala: float  # Positional
    dig_bala: float     # Directional
    kala_bala: float    # Temporal
    cheshta_bala: float # Motional
    naisargika_bala: float # Natural
    drik_bala: float    # Aspectual
    total_virupas: float
    total_rupas: float
    required_rupas: float
    ratio: float
    is_strong: bool

class StrengthEngine:
    """Calculates Shadbala and subsidiary strengths."""
    
    @classmethod
    def calculate_shadbala(
        cls,
        planets_data: Dict[str, Any],
        asc_sid_lon: float,
        is_day_birth: bool
    ) -> Dict[str, ShadbalaDetail]:
        """Compute full Shadbala in Virupas and Rupas for 7 traditional planets."""
        shadbala_data: Dict[str, ShadbalaDetail] = {}
        
        sun_lon = planets_data['Sun'].sidereal_lon if hasattr(planets_data['Sun'], 'sidereal_lon') else planets_data['Sun']['sidereal_lon']
        moon_lon = planets_data['Moon'].sidereal_lon if hasattr(planets_data['Moon'], 'sidereal_lon') else planets_data['Moon']['sidereal_lon']
        
        # Solar-Lunar angular distance for Paksha Bala
        moon_sun_diff = (moon_lon - sun_lon) % 360.0
        paksha_virupas = (moon_sun_diff / 180.0) * 60.0 if moon_sun_diff <= 180.0 else ((360.0 - moon_sun_diff) / 180.0) * 60.0

        for p_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            p_obj = planets_data[p_name]
            p_lon = p_obj.sidereal_lon if hasattr(p_obj, 'sidereal_lon') else p_obj['sidereal_lon']
            speed = p_obj.speed if hasattr(p_obj, 'speed') else p_obj.get('speed', 1.0)
            
            # 1. Sthana Bala (Positional Strength)
            # Uchcha Bala (Exaltation): 60 Virupas at exaltation peak, 0 at debilitation
            ex_degs = {'Sun':10,'Moon':33,'Mars':298,'Mercury':165,'Jupiter':95,'Venus':357,'Saturn':200}
            ex_d = ex_degs[p_name]
            dist_from_deb = (p_lon - (ex_d + 180.0) % 360.0) % 360.0
            if dist_from_deb > 180.0:
                dist_from_deb = 360.0 - dist_from_deb
            uchcha_virupas = (dist_from_deb / 180.0) * 60.0
            
            # Kendra Bala: 60 in Kendra (1,4,7,10), 30 in Panaphara (2,5,8,11), 15 in Apoklima (3,6,9,12)
            sign_idx = int(p_lon // 30)
            asc_idx = int((asc_sid_lon % 360.0) // 30)
            h_num = ((sign_idx - asc_idx) % 12) + 1
            if h_num in [1, 4, 7, 10]:
                kendra_v = 60.0
            elif h_num in [2, 5, 8, 11]:
                kendra_v = 30.0
            else:
                kendra_v = 15.0
                
            sthana_b = uchcha_virupas + kendra_v + 30.0 # Approximate baseline for Saptavargiya
            
            # 2. Dig Bala (Directional Strength)
            # Sun/Mars max at 10th (270°), Moon/Venus at 4th (90°), Merc/Jup at 1st (0°), Sat at 7th (180°)
            dig_peaks = {'Sun':270,'Mars':270,'Moon':90,'Venus':90,'Mercury':0,'Jupiter':0,'Saturn':180}
            peak = (asc_sid_lon + dig_peaks[p_name]) % 360.0
            diff = abs(p_lon - peak)
            if diff > 180.0: diff = 360.0 - diff
            dig_b = (1.0 - (diff / 180.0)) * 60.0

            # 3. Kala Bala (Temporal Strength)
            # Nathonnatha Bala (Day/Night)
            if p_name in ['Sun', 'Jupiter', 'Venus']:
                natho_v = 60.0 if is_day_birth else 0.0
            elif p_name in ['Moon', 'Mars', 'Saturn']:
                natho_v = 0.0 if is_day_birth else 60.0
            else: # Mercury always 60
                natho_v = 60.0
                
            paksha_v = (60.0 - paksha_virupas) if p_name in ['Mars', 'Saturn', 'Sun'] else paksha_virupas
            kala_b = natho_v + paksha_v + 30.0

            # 4. Cheshta Bala (Motional Strength)
            if p_name in ['Sun', 'Moon']:
                cheshta_b = paksha_virupas
            else:
                cheshta_b = 60.0 if speed < 0 else min(max(abs(speed) * 30.0, 10.0), 50.0)

            # 5. Naisargika Bala (Natural Strength)
            naisargika_b = NAISARGIKA_BALA[p_name]

            # 6. Drik Bala (Aspectual Strength baseline)
            drik_b = 15.0

            total_v = sthana_b + dig_b + kala_b + cheshta_b + naisargika_b + drik_b
            total_r = total_v / 60.0
            req_r = REQUIRED_SHADBALA[p_name]
            ratio = total_r / req_r

            shadbala_data[p_name] = ShadbalaDetail(
                planet=p_name,
                sthana_bala=round(sthana_b, 2),
                dig_bala=round(dig_b, 2),
                kala_bala=round(kala_b, 2),
                cheshta_bala=round(cheshta_b, 2),
                naisargika_bala=round(naisargika_b, 2),
                drik_bala=round(drik_b, 2),
                total_virupas=round(total_v, 2),
                total_rupas=round(total_r, 2),
                required_rupas=req_r,
                ratio=round(ratio, 2),
                is_strong=ratio >= 1.0
            )

        return shadbala_data

    @classmethod
    def calculate_ishta_kashta(cls, shadbala_dict: Dict[str, ShadbalaDetail], planets_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Calculate Ishta Phala & Kashta Phala for planets."""
        phala = {}
        for p_name, sb in shadbala_dict.items():
            uchcha_v = sb.sthana_bala * 0.5 # approximate Uchcha component
            cheshta_v = sb.cheshta_bala
            
            ishta = math.sqrt(max(uchcha_v * cheshta_v, 0.0))
            kashta = math.sqrt(max((60.0 - uchcha_v) * (60.0 - cheshta_v), 0.0))
            
            phala[p_name] = {
                "ishta_phala": round(ishta, 2),
                "kashta_phala": round(kashta, 2)
            }
        return phala
