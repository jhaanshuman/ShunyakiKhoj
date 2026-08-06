# -*- coding: utf-8 -*-
"""
panchang_api.py - Categorical Daily & Extended Panchang API Component
"""

from typing import Dict, Any
from datetime import datetime
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

import kundli_utils

def get_daily_panchang(date_str: str, time_str: str, place: str, lat: float = None, lon: float = None, tz_offset: float = 5.5) -> Dict[str, Any]:
    chart = kundli_utils.get_chart(
        date_str=date_str,
        time_str=time_str,
        place=place,
        zodiac="Sidereal",
        house_system="Whole Sign",
        ayanamsa="Lahiri",
        node_type="True"
    )
    sun_lon = chart.get('Sun').lon
    moon_lon = chart.get('Moon').lon
    b_date = datetime.strptime(date_str.replace('-', '/'), "%Y/%m/%d").date()
    
    panchang = kundli_utils.get_panchang(sun_lon, moon_lon, b_date, chart.lat, chart.lon, chart.utc_offset_hours)
    panchang_ext = kundli_utils.get_extended_panchang(sun_lon, moon_lon, b_date, chart.lat, chart.lon, chart.utc_offset_hours, chart.ayanamsa_val, chart.jd)
    choghadiya = kundli_utils.get_choghadiya_list(b_date, chart.lat, chart.lon, chart.utc_offset_hours)
    hora = kundli_utils.get_hora_list(b_date, chart.lat, chart.lon, chart.utc_offset_hours)
    
    return {
        "status": "success",
        "date": date_str,
        "place": place,
        "panchang": panchang,
        "panchang_extended": panchang_ext,
        "choghadiya": choghadiya,
        "hora": hora
    }
