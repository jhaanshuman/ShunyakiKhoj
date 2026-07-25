# -*- coding: utf-8 -*-
"""
Arudha Engine: Calculates Arudha Padas (AL, A2 to A11, UL) following Jaimini Sutras.
"""
from dataclasses import dataclass
from typing import Dict, Any, List
from .planets import SIGN_NAMES, SIGN_LORDS

@dataclass
class ArudhaPadaDetail:
    code: str
    house_number: int
    sign_index: int
    sign_name: str
    sign_lord: str
    in_house: int

class ArudhaEngine:
    """Computes Arudha Padas for houses H1 to H12."""
    
    @classmethod
    def calculate_arudhas(
        cls,
        asc_sign_name: str,
        planets_data: Dict[str, Any]
    ) -> Dict[str, ArudhaPadaDetail]:
        """Compute Arudha Padas AL, A2...A11, UL."""
        asc_sign_idx = SIGN_NAMES.index(asc_sign_name)
        arudhas: Dict[str, ArudhaPadaDetail] = {}
        
        labels = {
            1: "AL", 2: "A2", 3: "A3", 4: "A4", 5: "A5", 6: "A6",
            7: "A7", 8: "A8", 9: "A9", 10: "A10", 11: "A11", 12: "UL"
        }
        
        for h in range(1, 13):
            code = labels[h]
            # House sign index
            house_sign_idx = (asc_sign_idx + h - 1) % 12
            house_sign_name = SIGN_NAMES[house_sign_idx]
            lord_name = SIGN_LORDS[house_sign_name]
            
            # Find lord sign index
            lord_obj = planets_data.get(lord_name)
            if lord_obj and hasattr(lord_obj, 'sign_index'):
                lord_sign_idx = lord_obj.sign_index
            elif lord_obj and isinstance(lord_obj, dict):
                lord_sign_idx = lord_obj.get('sign_index', SIGN_NAMES.index(lord_obj.get('sign', 'Aries')))
            else:
                lord_sign_idx = house_sign_idx
                
            # Count from house sign to lord sign (inclusive: 1..12)
            dist = ((lord_sign_idx - house_sign_idx) % 12) + 1
            
            # Arudha sign = lord sign + dist - 1
            raw_arudha_idx = (lord_sign_idx + dist - 1) % 12
            
            # Jaimini Exceptions: If Arudha falls in 1st or 7th from house sign, shift by 10 signs (9 added)
            arudha_dist_from_house = ((raw_arudha_idx - house_sign_idx) % 12) + 1
            if arudha_dist_from_house == 1 or arudha_dist_from_house == 7:
                final_arudha_idx = (raw_arudha_idx + 9) % 12
            else:
                final_arudha_idx = raw_arudha_idx
                
            arudha_sign_name = SIGN_NAMES[final_arudha_idx]
            in_h = ((final_arudha_idx - asc_sign_idx) % 12) + 1
            
            arudhas[code] = ArudhaPadaDetail(
                code=code,
                house_number=h,
                sign_index=final_arudha_idx,
                sign_name=arudha_sign_name,
                sign_lord=SIGN_LORDS[arudha_sign_name],
                in_house=in_h
            )
            
        return arudhas
