# -*- coding: utf-8 -*-
"""
Panchanga Engine: Precision computations for Tithi, Nakshatra, Yoga, Karana, Vaara, and Muhurtas.
"""
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Dict, List, Any

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima / Amavasya"
]

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja",
    "Vanija", "Vishti (Bhadra)", "Shakuni", "Chatushpada", "Naga", "Kintughna"
]

VAARA_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

@dataclass
class PanchangaData:
    tithi_name: str
    tithi_number: int
    paksha: str
    tithi_completion_percent: float
    nakshatra_name: str
    nakshatra_number: int
    nakshatra_completion_percent: float
    yoga_name: str
    yoga_number: int
    karana_name: str
    karana_number: int
    vaara: str
    moon_phase: str
    rahu_kalam: str
    yamaganda: str
    gulika_kalam: str
    abhijit_muhurta: str

class PanchangaEngine:
    """Computes precision Panchanga elements and daily auspicious/inauspicious windows."""
    
    @classmethod
    def calculate_panchanga(
        cls,
        sun_sid_lon: float,
        moon_sid_lon: float,
        birth_dt: datetime,
        sunrise_jd: float = None,
        sunset_jd: float = None
    ) -> PanchangaData:
        """Compute full Panchanga elements."""
        sun_lon = sun_sid_lon % 360.0
        moon_lon = moon_sid_lon % 360.0
        
        # 1. Tithi: (Moon_lon - Sun_lon) % 360 / 12°
        diff_lon = (moon_lon - sun_lon) % 360.0
        tithi_val = diff_lon / 12.0
        tithi_idx = int(tithi_val) # 0..29
        tithi_pct = round((tithi_val - tithi_idx) * 100.0, 2)
        
        paksha = "Shukla Paksha" if tithi_idx < 15 else "Krishna Paksha"
        raw_tithi_num = (tithi_idx % 15) + 1
        tithi_name = f"{paksha} {TITHI_NAMES[raw_tithi_num - 1]}"
        
        # 2. Nakshatra: Moon_lon / 13°20'
        nak_val = moon_lon / (360.0 / 27.0)
        nak_idx = int(nak_val)
        nak_pct = round((nak_val - nak_idx) * 100.0, 2)
        from .planets import NAKSHATRAS
        nak_name = NAKSHATRA_LORDS = NAKSHATRAS[nak_idx % 27]
        
        # 3. Yoga: (Sun_lon + Moon_lon) % 360 / 13°20'
        yoga_val = ((sun_lon + moon_lon) % 360.0) / (360.0 / 27.0)
        yoga_idx = int(yoga_val)
        yoga_name = YOGA_NAMES[yoga_idx % 27]
        
        # 4. Karana: (Moon_lon - Sun_lon) % 360 / 6°
        karana_val = diff_lon / 6.0
        karana_idx = int(karana_val) # 0..59
        if karana_idx == 0:
            karana_name = "Kintughna"
        elif karana_idx >= 57:
            fixed = ["Shakuni", "Chatushpada", "Naga"]
            karana_name = fixed[karana_idx - 57]
        else:
            movable = ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti (Bhadra)"]
            karana_name = movable[(karana_idx - 1) % 7]

        # 5. Vaara & Moon phase
        vaara_idx = birth_dt.weekday() # 0=Mon, 6=Sun
        # convert to Sun=0 .. Sat=6
        vaara_idx_sun = (vaara_idx + 1) % 7
        vaara_name = VAARA_NAMES[vaara_idx_sun]
        
        if diff_lon < 15 or diff_lon > 345:
            moon_phase = "New Moon (Amavasya)"
        elif 165 < diff_lon < 195:
            moon_phase = "Full Moon (Purnima)"
        elif diff_lon < 180:
            moon_phase = "Waxing Crescent / Gibbous"
        else:
            moon_phase = "Waning Gibbous / Crescent"

        # 6. Rahu Kalam, Yamaganda, Gulika Kalam offsets (8 parts of daytime)
        # Offsets in 1/8th parts of daytime for days Sun=0..Sat=6
        rahu_offsets = [7, 1, 6, 4, 5, 3, 2]     # Sun, Mon, Tue, Wed, Thu, Fri, Sat
        yama_offsets = [4, 3, 2, 1, 0, 5, 6]
        guli_offsets = [6, 4, 3, 2, 1, 0, 5]

        # Default 06:00 to 18:00 if sunrise/sunset not available
        sr = birth_dt.replace(hour=6, minute=0, second=0)
        ss = birth_dt.replace(hour=18, minute=0, second=0)
        day_dur_sec = (ss - sr).total_seconds()
        part_sec = day_dur_sec / 8.0

        r_start = sr + timedelta(seconds=part_sec * rahu_offsets[vaara_idx_sun])
        r_end = r_start + timedelta(seconds=part_sec)
        rahu_str = f"{r_start.strftime('%H:%M')} - {r_end.strftime('%H:%M')}"

        y_start = sr + timedelta(seconds=part_sec * yama_offsets[vaara_idx_sun])
        y_end = y_start + timedelta(seconds=part_sec)
        yama_str = f"{y_start.strftime('%H:%M')} - {y_end.strftime('%H:%M')}"

        g_start = sr + timedelta(seconds=part_sec * guli_offsets[vaara_idx_sun])
        g_end = g_start + timedelta(seconds=part_sec)
        guli_str = f"{g_start.strftime('%H:%M')} - {g_end.strftime('%H:%M')}"

        # Abhijit Muhurta (8th Muhurta around midday)
        midday = sr + timedelta(seconds=day_dur_sec / 2.0)
        abh_start = midday - timedelta(minutes=24)
        abh_end = midday + timedelta(minutes=24)
        abh_str = f"{abh_start.strftime('%H:%M')} - {abh_end.strftime('%H:%M')}"

        return PanchangaData(
            tithi_name=tithi_name,
            tithi_number=tithi_idx + 1,
            paksha=paksha,
            tithi_completion_percent=tithi_pct,
            nakshatra_name=nak_name,
            nakshatra_number=nak_idx + 1,
            nakshatra_completion_percent=nak_pct,
            yoga_name=yoga_name,
            yoga_number=yoga_idx + 1,
            karana_name=karana_name,
            karana_number=karana_idx + 1,
            vaara=vaara_name,
            moon_phase=moon_phase,
            rahu_kalam=rahu_str,
            yamaganda=yama_str,
            gulika_kalam=guli_str,
            abhijit_muhurta=abh_str
        )
