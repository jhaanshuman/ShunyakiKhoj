from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from datetime import datetime

# Append local path so we can import from kundli_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import kundli_utils

app = FastAPI(title="Vedic Astrology API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BirthDetails(BaseModel):
    date: str  # YYYY/MM/DD
    time: str  # HH:MM
    place: str
    ayanamsa: str = "Lahiri"
    node_type: str = "True"
    zodiac: str = "Sidereal"

@app.post("/api/calculate")
@app.post("/")
def calculate_chart(details: BirthDetails):
    try:
        details.date = details.date.replace('-', '/')
        # 1. Compute Chart
        chart = kundli_utils.get_chart(
            date_str=details.date,
            time_str=details.time,
            place=details.place,
            zodiac=details.zodiac,
            house_system="Whole Sign",
            ayanamsa=details.ayanamsa,
            node_type=details.node_type
        )
        
        # 2. Get Ascendant and Planet Placements (D1)
        asc_sign, asc_deg = kundli_utils.get_ascendant(chart)
        planets_data = kundli_utils.get_planet_positions(chart)
        
        # 3. Compute Shodashvarga Divisional Charts (D1 to D60)
        divisions = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 30, 40, 45, 60]
        div_charts = {}
        for div in divisions:
            div_charts[f"D{div}"] = {}
            for p_name in kundli_utils.PLANETS:
                p_obj = chart.get(p_name)
                div_charts[f"D{div}"][p_name] = {
                    "sign": kundli_utils.get_divisional_chart_sign(p_obj.lon, div),
                    "lon": round(p_obj.lon % 30, 2)
                }
            # Add Ascendant
            asc_obj = chart.get('Asc')
            div_charts[f"D{div}"]['Asc'] = {
                "sign": kundli_utils.get_divisional_chart_sign(asc_obj.lon, div),
                "lon": round(asc_obj.lon % 30, 2)
            }
        
        # 4. Compute Panchang
        sun_lon = chart.get('Sun').lon
        moon_lon = chart.get('Moon').lon
        birth_date = datetime.strptime(details.date, "%Y/%m/%d").date()
        panchang = kundli_utils.get_panchang(sun_lon, moon_lon, birth_date, chart.lat, chart.lon, chart.utc_offset_hours)
        panchang_ext = kundli_utils.get_extended_panchang(sun_lon, moon_lon, birth_date, chart.lat, chart.lon, chart.utc_offset_hours, chart.ayanamsa_val, chart.jd)
        
        # 5. Compute Choghadiya, Hora & Regional months
        choghadiya = kundli_utils.get_choghadiya_list(birth_date, chart.lat, chart.lon, chart.utc_offset_hours)
        hora = kundli_utils.get_hora_list(birth_date, chart.lat, chart.lon, chart.utc_offset_hours)
        
        sun_sign_idx = kundli_utils.SIGN_NAMES.index(planets_data['Sun']['sign'])
        reg_months = kundli_utils.REGIONAL_MONTHS[sun_sign_idx]
        lunar_month = kundli_utils.LUNAR_MONTHS[sun_sign_idx]
        
        regional_panchang = {
            "tamil": reg_months['tamil'],
            "malayalam": reg_months['malayalam'],
            "bengali": reg_months['bengali'],
            "odia": reg_months['odia'],
            "lunar_month": lunar_month,
            "shaka_year": birth_date.year - 78,
            "vikrama_year": birth_date.year + 57,
            "kali_year": birth_date.year + 3101
        }
        
        # 6. Houses
        houses = kundli_utils.get_house_details(chart)
        
        return {
            "status": "success",
            "pob": chart.formatted_pob,
            "timezone": chart.timezone,
            "utc_offset": chart.utc_offset_hours,
            "ayanamsa": chart.ayanamsa,
            "ayanamsa_val": round(chart.ayanamsa_val, 4),
            "ascendant": {
                "sign": asc_sign,
                "degree": round(asc_deg, 2)
            },
            "d1_chart": planets_data,
            "divisional_charts": div_charts,
            "panchang": panchang,
            "panchang_extended": panchang_ext,
            "choghadiya": choghadiya,
            "hora": hora,
            "regional": regional_panchang,
            "houses": houses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class MonthDetails(BaseModel):
    year: int
    month: int
    place: str
    ayanamsa: str = "Lahiri"
    node_type: str = "True"
    zodiac: str = "Sidereal"

@app.post("/api/calculate_month")
def calculate_month(details: MonthDetails):
    import calendar
    try:
        results = {}
        # Get number of days in the month
        num_days = calendar.monthrange(details.year, details.month)[1]
        
        for d in range(1, num_days + 1):
            date_str = f"{details.year}/{details.month:02d}/{d:02d}"
            
            chart = kundli_utils.get_chart(
                date_str=date_str,
                time_str="12:00",
                place=details.place,
                zodiac=details.zodiac,
                house_system="Whole Sign",
                ayanamsa=details.ayanamsa,
                node_type=details.node_type
            )
            
            sun_lon = chart.get('Sun').lon
            moon_lon = chart.get('Moon').lon
            birth_date = datetime.strptime(date_str, "%Y/%m/%d").date()
            
            panchang = kundli_utils.get_panchang(sun_lon, moon_lon, birth_date, chart.lat, chart.lon, chart.utc_offset_hours)
            panchang_ext = kundli_utils.get_extended_panchang(sun_lon, moon_lon, birth_date, chart.lat, chart.lon, chart.utc_offset_hours, chart.ayanamsa_val, chart.jd)
            
            sun_sign_idx = kundli_utils.SIGN_NAMES.index(kundli_utils.get_planet_positions(chart)['Sun']['sign'])
            reg_months = kundli_utils.REGIONAL_MONTHS[sun_sign_idx]
            lunar_month = kundli_utils.LUNAR_MONTHS[sun_sign_idx]
            
            regional_panchang = {
                "tamil": reg_months['tamil'],
                "malayalam": reg_months['malayalam'],
                "bengali": reg_months['bengali'],
                "odia": reg_months['odia'],
                "lunar_month": lunar_month,
                "shaka_year": birth_date.year - 78,
                "vikrama_year": birth_date.year + 57,
                "kali_year": birth_date.year + 3101
            }
            
            results[f"{details.year}-{details.month:02d}-{d:02d}"] = {
                "status": "success",
                "panchang": panchang,
                "panchang_extended": panchang_ext,
                "regional": regional_panchang
            }
            
        return {
            "status": "success",
            "month_data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import json

if os.environ.get('VERCEL') or os.path.exists("/tmp"):
    CACHE_FILE = "/tmp/cached_panchang.json"
else:
    CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cached_panchang.json")

def get_new_delhi_panchang_cached():
    today_str = datetime.now().strftime("%Y/%m/%d")
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
            if cached_data.get("date") == today_str:
                return cached_data.get("data")
        except Exception as e:
            print("Failed to read cache:", e)

    try:
        chart = kundli_utils.get_chart(
            date_str=today_str,
            time_str="12:00",
            place="New Delhi, India",
            zodiac="Sidereal",
            house_system="Whole Sign",
            ayanamsa="Lahiri",
            node_type="True"
        )
        asc_sign, asc_deg = kundli_utils.get_ascendant(chart)
        planets_data = kundli_utils.get_planet_positions(chart)
        
        divisions = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 30, 40, 45, 60]
        div_charts = {}
        for div in divisions:
            div_charts[f"D{div}"] = {}
            for p_name in kundli_utils.PLANETS:
                p_obj = chart.get(p_name)
                div_charts[f"D{div}"][p_name] = {
                    "sign": kundli_utils.get_divisional_chart_sign(p_obj.lon, div),
                    "lon": round(p_obj.lon % 30, 2)
                }
            asc_obj = chart.get('Asc')
            div_charts[f"D{div}"]['Asc'] = {
                "sign": kundli_utils.get_divisional_chart_sign(asc_obj.lon, div),
                "lon": round(asc_obj.lon % 30, 2)
            }
        
        sun_lon = chart.get('Sun').lon
        moon_lon = chart.get('Moon').lon
        birth_date = datetime.now().date()
        panchang = kundli_utils.get_panchang(sun_lon, moon_lon, birth_date, chart.lat, chart.lon, chart.utc_offset_hours)
        panchang_ext = kundli_utils.get_extended_panchang(sun_lon, moon_lon, birth_date, chart.lat, chart.lon, chart.utc_offset_hours, chart.ayanamsa_val, chart.jd)
        choghadiya = kundli_utils.get_choghadiya_list(birth_date, chart.lat, chart.lon, chart.utc_offset_hours)
        hora = kundli_utils.get_hora_list(birth_date, chart.lat, chart.lon, chart.utc_offset_hours)
        
        sun_sign_idx = kundli_utils.SIGN_NAMES.index(planets_data['Sun']['sign'])
        reg_months = kundli_utils.REGIONAL_MONTHS[sun_sign_idx]
        lunar_month = kundli_utils.LUNAR_MONTHS[sun_sign_idx]
        
        regional_panchang = {
            "tamil": reg_months['tamil'],
            "malayalam": reg_months['malayalam'],
            "bengali": reg_months['bengali'],
            "odia": reg_months['odia'],
            "lunar_month": lunar_month,
            "shaka_year": birth_date.year - 78,
            "vikrama_year": birth_date.year + 57,
            "kali_year": birth_date.year + 3101
        }
        
        houses = kundli_utils.get_house_details(chart)
        
        response_data = {
            "status": "success",
            "pob": chart.formatted_pob,
            "timezone": chart.timezone,
            "utc_offset": chart.utc_offset_hours,
            "ayanamsa": chart.ayanamsa,
            "ayanamsa_val": round(chart.ayanamsa_val, 4),
            "ascendant": {
                "sign": asc_sign,
                "degree": round(asc_deg, 2)
            },
            "d1_chart": planets_data,
            "divisional_charts": div_charts,
            "panchang": panchang,
            "panchang_extended": panchang_ext,
            "choghadiya": choghadiya,
            "hora": hora,
            "regional": regional_panchang,
            "houses": houses
        }
        
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"date": today_str, "data": response_data}, f, ensure_ascii=False, indent=2)
            
        return response_data
    except Exception as e:
        print("Failed to calculate cache:", e)
        return None

@app.get("/api/cached_panchang")
def get_cached_panchang():
    data = get_new_delhi_panchang_cached()
    if data:
        return data
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve or compute cached Panchang.")


import threading
import time
from datetime import datetime

def run_cache_pregenerator():
    print("Pregenerator thread started. Waiting to refresh New Delhi cache daily at 12:01 AM...")
    while True:
        try:
            now = datetime.now()
            # Run at 12:01 AM local time
            if now.hour == 0 and now.minute == 1:
                print(f"[{datetime.now()}] Pregenerating New Delhi panchang cache...")
                get_new_delhi_panchang_cached()
                time.sleep(60) # Sleep 60s to prevent multiple runs in same minute
        except Exception as e:
            print("Pregenerator error:", e)
        time.sleep(15)

# Start background daemon thread
threading.Thread(target=run_cache_pregenerator, daemon=True).start()

