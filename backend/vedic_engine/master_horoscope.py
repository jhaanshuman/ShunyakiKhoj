# -*- coding: utf-8 -*-
"""
Master Horoscope Engine Wrapper (v5.0 Redirect).
Provides backward compatibility while delegating 100% of calculations to MasterHoroscopeBuilderV5.
"""

from typing import Dict, Any, List
from .orchestrator.master_builder_v5 import MasterHoroscopeBuilderV5

class MasterHoroscopeBuilder:
    """Canonical wrapper delegating to MasterHoroscopeBuilderV5."""
    
    @classmethod
    def build_master_horoscope(
        cls,
        name: str,
        gender: str,
        dob_str: str,
        tob_str: str,
        place: str,
        lat: float,
        lon: float,
        tz_offset: float = 5.5,
        ayanamsa_name: str = "Lahiri",
        node_type: str = "True",
        house_system: str = "Whole Sign",
        custom_ayanamsa_offset: float = 0.0,
        requested_modules: List[str] = None
    ) -> Dict[str, Any]:
        """Delegate directly to MasterHoroscopeBuilderV5 for single source of truth."""
        return MasterHoroscopeBuilderV5.build_master_horoscope(
            name=name,
            gender=gender,
            dob_str=dob_str,
            tob_str=tob_str,
            place=place,
            lat=lat,
            lon=lon,
            tz_offset=tz_offset,
            ayanamsa_name=ayanamsa_name,
            node_type=node_type,
            house_system=house_system,
            requested_modules=requested_modules
        )
