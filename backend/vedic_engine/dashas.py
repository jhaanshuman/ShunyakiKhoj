# -*- coding: utf-8 -*-
"""
Dasha Engine: Computes 5-tier Vimshottari, Yogini, Ashtottari, and Chara Dashas dynamically.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from .planets import NAKSHATRA_LORDS

# Vimshottari Sequence & Duration in Years
VIMSHOTTARI_SEQ = [
    ('Ketu', 7.0), ('Venus', 20.0), ('Sun', 6.0), ('Moon', 10.0),
    ('Mars', 7.0), ('Rahu', 18.0), ('Jupiter', 16.0), ('Saturn', 19.0), ('Mercury', 17.0)
]
TOTAL_VIMSHOTTARI_YEARS = 120.0

YOGINI_SEQ = [
    ('Mangala', 1.0, 'Moon'), ('Pingala', 2.0, 'Sun'), ('Dhanya', 3.0, 'Jupiter'),
    ('Bhramari', 4.0, 'Mars'), ('Bhadrika', 5.0, 'Mercury'), ('Ulka', 6.0, 'Saturn'),
    ('Siddha', 7.0, 'Venus'), ('Sankata', 8.0, 'Rahu')
]
TOTAL_YOGINI_YEARS = 36.0

@dataclass
class DashaPeriod:
    lord: str
    start_date: str
    end_date: str
    duration_years: float
    sub_periods: List[Any] = None

class DashaEngine:
    """Calculates Vimshottari, Yogini, Ashtottari, and Chara dashas dynamically."""
    
    @classmethod
    def calculate_vimshottari(
        cls,
        moon_sid_lon: float,
        birth_dt: datetime,
        depth: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Calculate 5-tier Vimshottari Dasha (Mahadasha -> Antar -> Pratyantar -> Sookshma -> Prana).
        """
        # Nakshatra span = 13° 20' = 13.333333333333334 degrees
        nak_span = 360.0 / 27.0
        nak_idx = int((moon_sid_lon % 360.0) // nak_span)
        rem_deg = (moon_sid_lon % 360.0) % nak_span
        elapsed_fraction = rem_deg / nak_span
        balance_fraction = 1.0 - elapsed_fraction
        
        start_lord = NAKSHATRA_LORDS[nak_idx % 27]
        
        # Locate index in Vimshottari sequence
        lord_names = [item[0] for item in VIMSHOTTARI_SEQ]
        start_idx = lord_names.index(start_lord)
        
        mahadashas: List[Dict[str, Any]] = []
        curr_dt = birth_dt
        
        for i in range(9):
            idx = (start_idx + i) % 9
            lord, years = VIMSHOTTARI_SEQ[idx]
            
            if i == 0:
                duration_years = years * balance_fraction
            else:
                duration_years = years
                
            duration_days = duration_years * 365.2425
            end_dt = curr_dt + timedelta(days=duration_days)
            
            md_dict = {
                "lord": lord,
                "start": curr_dt.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "duration_years": round(duration_years, 3),
                "antardashas": []
            }
            
            if depth >= 2:
                md_dict["antardashas"] = cls._calculate_sub_dashas(
                    parent_lord_idx=idx,
                    parent_duration_years=duration_years,
                    parent_start_dt=curr_dt,
                    current_depth=2,
                    max_depth=depth
                )

            mahadashas.append(md_dict)
            curr_dt = end_dt

        return mahadashas

    @classmethod
    def _calculate_sub_dashas(
        cls,
        parent_lord_idx: int,
        parent_duration_years: float,
        parent_start_dt: datetime,
        current_depth: int,
        max_depth: int
    ) -> List[Dict[str, Any]]:
        sub_list = []
        curr_dt = parent_start_dt
        
        for j in range(9):
            sub_idx = (parent_lord_idx + j) % 9
            sub_lord, sub_years = VIMSHOTTARI_SEQ[sub_idx]
            
            sub_duration_years = (parent_duration_years * sub_years) / TOTAL_VIMSHOTTARI_YEARS
            sub_duration_days = sub_duration_years * 365.2425
            end_dt = curr_dt + timedelta(days=sub_duration_days)
            
            sub_dict = {
                "lord": sub_lord,
                "start": curr_dt.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "duration_days": round(sub_duration_days, 2)
            }
            
            if current_depth < max_depth:
                sub_key = ["antardashas", "pratyantardashas", "sookshmadashas", "pranadashas"][current_depth - 1]
                sub_dict[sub_key] = cls._calculate_sub_dashas(
                    parent_lord_idx=sub_idx,
                    parent_duration_years=sub_duration_years,
                    parent_start_dt=curr_dt,
                    current_depth=current_depth + 1,
                    max_depth=max_depth
                )

            sub_list.append(sub_dict)
            curr_dt = end_dt

        return sub_list

    @classmethod
    def calculate_yogini(
        cls,
        moon_sid_lon: float,
        birth_dt: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate 36-year cycle Yogini Dasha."""
        nak_span = 360.0 / 27.0
        nak_idx = int((moon_sid_lon % 360.0) // nak_span) + 1 # 1-27
        rem_deg = (moon_sid_lon % 360.0) % nak_span
        balance_fraction = 1.0 - (rem_deg / nak_span)
        
        # Yogini index formula = (Nakshatra index + 3) % 8
        yogini_idx = (nak_idx + 3) % 8
        
        yoginis = []
        curr_dt = birth_dt
        for i in range(8):
            idx = (yogini_idx + i) % 8
            y_name, years, ruler = YOGINI_SEQ[idx]
            dur_years = years * balance_fraction if i == 0 else years
            dur_days = dur_years * 365.2425
            end_dt = curr_dt + timedelta(days=dur_days)
            
            yoginis.append({
                "yogini": y_name,
                "ruler": ruler,
                "start": curr_dt.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "duration_years": round(dur_years, 2)
            })
            curr_dt = end_dt
            
        return yoginis
