# -*- coding: utf-8 -*-
"""
horoscope_api.py - Categorical Horoscope & Chart Calculation API Component
"""

from typing import Dict, Any, List, Optional
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from vedic_engine.orchestrator.master_builder_v5 import MasterHoroscopeBuilderV5

def calculate_horoscope(
    name: str,
    gender: str,
    dob: str,
    tob: str,
    place: str,
    lat: float,
    lon: float,
    tz_offset: float = 5.5,
    ayanamsa: str = "Lahiri",
    node_type: str = "True",
    house_system: str = "Whole Sign",
    requested_modules: Optional[List[str]] = None
) -> Dict[str, Any]:
    return MasterHoroscopeBuilderV5.build_master_horoscope(
        name=name,
        gender=gender,
        dob_str=dob,
        tob_str=tob,
        place=place,
        lat=lat,
        lon=lon,
        tz_offset=tz_offset,
        ayanamsa_name=ayanamsa,
        node_type=node_type,
        house_system=house_system,
        requested_modules=requested_modules or ["ALL"]
    )
