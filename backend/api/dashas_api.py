# -*- coding: utf-8 -*-
"""
dashas_api.py - Categorical Dasha Systems API Component
"""

from typing import Dict, Any
from datetime import datetime
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

import kundli_utils

def get_vimshottari_dasha(date_str: str, time_str: str, place: str, ayanamsa: str = "Lahiri") -> Dict[str, Any]:
    clean_date = date_str.replace('-', '/')
    chart = kundli_utils.get_chart(
        date_str=clean_date,
        time_str=time_str,
        place=place,
        zodiac="Sidereal",
        house_system="Whole Sign",
        ayanamsa=ayanamsa,
        node_type="True"
    )
    b_date = datetime.strptime(clean_date, "%Y/%m/%d").date()
    moon_lon = chart.get('Moon').lon
    dasha_data = kundli_utils.get_vimshottari_dasha(moon_lon, b_date)
    return {
        "status": "success",
        "system": "Vimshottari",
        **dasha_data
    }
