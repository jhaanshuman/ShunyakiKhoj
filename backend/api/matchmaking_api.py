# -*- coding: utf-8 -*-
"""
matchmaking_api.py - Categorical Matchmaking & Ashtakoot Guna Milan API Component
"""

from typing import Dict, Any
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

import kundli_utils

def calculate_matchmaking(
    boy_date: str, boy_time: str, boy_place: str,
    girl_date: str, girl_time: str, girl_place: str,
    ayanamsa: str = "Lahiri"
) -> Dict[str, Any]:
    b_date = boy_date.replace('-', '/')
    g_date = girl_date.replace('-', '/')
    
    boy_chart = kundli_utils.get_chart(date_str=b_date, time_str=boy_time, place=boy_place, ayanamsa=ayanamsa)
    girl_chart = kundli_utils.get_chart(date_str=g_date, time_str=girl_time, place=girl_place, ayanamsa=ayanamsa)
    
    boy_planets = kundli_utils.get_planet_positions(boy_chart)
    girl_planets = kundli_utils.get_planet_positions(girl_chart)
    
    milan = kundli_utils.get_milan_score(
        boy_chart.get('Moon').lon,
        girl_chart.get('Moon').lon,
        boy_planets['Moon']['sign'],
        girl_planets['Moon']['sign']
    )
    
    return {
        "status": "success",
        "boy": {"nakshatra": milan['boy_nakshatra'], "rashi": milan['boy_rashi']},
        "girl": {"nakshatra": milan['girl_nakshatra'], "rashi": milan['girl_rashi']},
        "milan": milan
    }
