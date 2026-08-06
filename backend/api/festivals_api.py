# -*- coding: utf-8 -*-
"""
festivals_api.py - Categorical Festivals & Fasts Scanner API Component
"""

from typing import Dict, Any, Optional
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

import api.calculate as calc_module

def query_festivals(year: Optional[int] = None, month: Optional[int] = None, date: Optional[str] = None) -> Dict[str, Any]:
    return calc_module.query_festivals(year=year, month=month, date=date)
