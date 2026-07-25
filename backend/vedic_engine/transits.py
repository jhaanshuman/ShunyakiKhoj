# -*- coding: utf-8 -*-
"""
Transit Engine: Real-time Gochar computations, Sade Sati, and Transit Aspects.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any
from .planets import SIGN_NAMES

# Benefic Transit Houses from Moon Sign for 7 Planets
BENEFIC_TRANSIT_HOUSES = {
    'Sun': [3, 6, 10, 11],
    'Moon': [1, 3, 6, 7, 10, 11],
    'Mars': [3, 6, 11],
    'Mercury': [2, 4, 6, 8, 10, 11],
    'Jupiter': [2, 5, 7, 9, 11],
    'Venus': [1, 2, 3, 4, 5, 8, 9, 11, 12],
    'Saturn': [3, 6, 11],
    'Rahu': [3, 6, 11],
    'Ketu': [3, 6, 11]
}

@dataclass
class TransitDetail:
    planet: str
    transit_sign: str
    transit_degree: float
    house_from_moon: int
    house_from_lagna: int
    is_benefic_transit: bool

class TransitEngine:
    """Calculates Gochar transit effects against Natal Chart."""
    
    @classmethod
    def calculate_gochar(
        cls,
        natal_moon_sign_idx: int,
        natal_asc_sign_idx: int,
        transit_planets_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute transit placements and Sade Sati status."""
        transit_details: Dict[str, TransitDetail] = {}
        
        for p_name, p_obj in transit_planets_data.items():
            p_lon = p_obj.sidereal_lon if hasattr(p_obj, 'sidereal_lon') else p_obj['sidereal_lon']
            t_sign_idx = int((p_lon % 360.0) // 30)
            t_sign_name = SIGN_NAMES[t_sign_idx]
            t_deg = p_lon % 30.0
            
            h_moon = ((t_sign_idx - natal_moon_sign_idx) % 12) + 1
            h_lagna = ((t_sign_idx - natal_asc_sign_idx) % 12) + 1
            
            is_benefic = h_moon in BENEFIC_TRANSIT_HOUSES.get(p_name, [])
            
            transit_details[p_name] = TransitDetail(
                planet=p_name,
                transit_sign=t_sign_name,
                transit_degree=round(t_deg, 2),
                house_from_moon=h_moon,
                house_from_lagna=h_lagna,
                is_benefic_transit=is_benefic
            )

        # Sade Sati analysis
        saturn_h_moon = transit_details['Saturn'].house_from_moon
        sade_sati_active = saturn_h_moon in [12, 1, 2]
        sade_sati_phase = None
        if saturn_h_moon == 12:
            sade_sati_phase = "1st Phase (Rising - 12th from Moon)"
        elif saturn_h_moon == 1:
            sade_sati_phase = "2nd Phase (Peak - 1st house Moon)"
        elif saturn_h_moon == 2:
            sade_sati_phase = "3rd Phase (Setting - 2nd from Moon)"
            
        ashtama_shani = saturn_h_moon == 8
        kantaka_shani = saturn_h_moon in [1, 4, 8, 10]

        return {
            "transits": transit_details,
            "sade_sati": {
                "is_active": sade_sati_active,
                "phase": sade_sati_phase,
                "ashtama_shani": ashtama_shani,
                "kantaka_shani": kantaka_shani
            }
        }
