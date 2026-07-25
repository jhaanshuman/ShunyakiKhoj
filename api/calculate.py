from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import json
import hashlib
import threading
from datetime import datetime

# Append root and backend directories to path
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.append(backend_dir)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vedic_engine.master_horoscope import MasterHoroscopeBuilder
from database import EngineDatabase
import kundli_utils

app = FastAPI(title="Vedic Astrology API", version="2.2.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from vedic_engine.orchestrator.master_builder_v5 import MasterHoroscopeBuilderV5

class CalculationOptions(BaseModel):
    ayanamsa: str = "Lahiri"
    node_type: str = "True"
    house_system: str = "Whole Sign"
    zodiac: str = "Sidereal"
    dasha_systems: List[str] = ["ALL"]
    yoga_depth: str = "Full"
    varga_list: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20, 24, 27, 30, 40, 45, 60]
    include_source_texts: bool = True

class BirthDetails(BaseModel):
    name: str = "Native"
    gender: str = "Male"
    date: str  # YYYY/MM/DD or YYYY-MM-DD
    time: str  # HH:MM
    place: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz_offset: float = 5.5
    ayanamsa: str = "Lahiri"
    node_type: str = "True"
    house_system: str = "Whole Sign"
    zodiac: str = "Sidereal"

class UniversalCalculateRequest(BaseModel):
    birth_details: Optional[BirthDetails] = None
    calculation_options: Optional[CalculationOptions] = CalculationOptions()
    requested_modules: List[str] = ["ALL"]
    partner_birth_details: Optional[BirthDetails] = None
    # Backward compatibility for direct flat parameters
    name: Optional[str] = None
    gender: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    place: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz_offset: Optional[float] = 5.5
    ayanamsa: Optional[str] = None
    node_type: Optional[str] = None
    house_system: Optional[str] = None

@app.post("/api/calculate")
@app.post("/")
def calculate_chart(request: Request, body: Dict[str, Any]):
    try:
        # Flexible parsing supporting both v5.0 nested JSON and v4.0 flat JSON
        birth_dict = body.get('birth_details', {})
        calc_options = body.get('calculation_options', {})
        requested_modules = body.get('requested_modules', ["ALL"])
        partner_dict = body.get('partner_birth_details', None)

        # Extract fields from nested birth_details or root body
        name = birth_dict.get('name') or body.get('name', 'Native')
        gender = birth_dict.get('gender') or body.get('gender', 'Male')
        date_str = birth_dict.get('date') or body.get('date', '1990/01/01')
        time_str = birth_dict.get('time') or body.get('time', '12:00')
        place = birth_dict.get('place') or body.get('place', 'New Delhi')
        lat = birth_dict.get('lat') if birth_dict.get('lat') is not None else body.get('lat')
        lon = birth_dict.get('lon') if birth_dict.get('lon') is not None else body.get('lon')
        tz_offset = birth_dict.get('tz_offset') or body.get('tz_offset', 5.5)

        ayanamsa = calc_options.get('ayanamsa') or birth_dict.get('ayanamsa') or body.get('ayanamsa', 'Lahiri')
        node_type = calc_options.get('node_type') or birth_dict.get('node_type') or body.get('node_type', 'True')
        house_system = calc_options.get('house_system') or birth_dict.get('house_system') or body.get('house_system', 'Whole Sign')

        clean_date = str(date_str).replace('-', '/')

        # Geocode lat/lon if not provided
        if lat is None or lon is None:
            g_lat, g_lon, g_tz, _ = kundli_utils.resolve_place(place)
            lat = g_lat
            lon = g_lon
            tz_offset = g_tz

        # Settings hash for database cache
        settings_str = f"{clean_date}_{time_str}_{lat:.4f}_{lon:.4f}_{tz_offset}_{ayanamsa}_{node_type}_{house_system}_{json.dumps(requested_modules)}"
        settings_hash = hashlib.sha256(settings_str.encode('utf-8')).hexdigest()[:16]

        # Check DB Cache
        cached = EngineDatabase.get_cached_horoscope(settings_hash)
        if cached:
            cached['status'] = 'success'
            return cached

        # Calculate Master Horoscope v5.0
        master_obj = MasterHoroscopeBuilderV5.build_master_horoscope(
            name=name,
            gender=gender,
            dob_str=clean_date,
            tob_str=time_str,
            place=place,
            lat=lat,
            lon=lon,
            tz_offset=tz_offset,
            ayanamsa_name=ayanamsa,
            node_type=node_type,
            house_system=house_system,
            requested_modules=requested_modules,
            partner_birth_details=partner_dict
        )

        # Backward-compatible d1_chart flat object
        master_obj['status'] = 'success'
        asc_sign_idx = int(master_obj['houses']['ascendant_sidereal_lon'] / 30.0) % 12
        d1_flat = {}
        for p_name, p_data in master_obj['planets'].items():
            h_num = p_data.get('house', ((p_data['sign_index'] - asc_sign_idx + 12) % 12) + 1)
            d1_flat[p_name] = {
                'sign': p_data['sign_name'],
                'degree': p_data['sign_degree'],
                'longitude': p_data['sidereal_lon'],
                'nakshatra': p_data['nakshatra_name'],
                'pada': p_data['pada'],
                'house': h_num,
                'is_retrograde': p_data['is_retrograde'],
                'is_combust': p_data['is_combust']
            }
        master_obj['d1_chart'] = d1_flat

        # Save to cache asynchronously or synchronously
        try:
            EngineDatabase.save_cached_horoscope(settings_hash, master_obj)
        except Exception:
            pass

        return master_obj
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/dasha")
def calculate_dasha(details: BirthDetails):
    """Dedicated dasha endpoint (also embedded in /api/calculate)."""
    try:
        details.date = details.date.replace('-', '/')
        chart = kundli_utils.get_chart(
            date_str=details.date, time_str=details.time, place=details.place,
            zodiac=details.zodiac, house_system="Whole Sign",
            ayanamsa=details.ayanamsa, node_type=details.node_type
        )
        birth_date = datetime.strptime(details.date, "%Y/%m/%d").date()
        moon_lon = chart.get('Moon').lon
        dasha_data = kundli_utils.get_vimshottari_dasha(moon_lon, birth_date)
        return {"status": "success", **dasha_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MatchDetails(BaseModel):
    boy_date: str
    boy_time: str
    boy_place: str
    girl_date: str
    girl_time: str
    girl_place: str
    ayanamsa: str = "Lahiri"
    node_type: str = "True"
    zodiac: str = "Sidereal"


@app.post("/api/match")
def calculate_match(details: MatchDetails):
    """Ashtakoot Guna Milan endpoint."""
    try:
        boy_date = details.boy_date.replace('-', '/')
        girl_date = details.girl_date.replace('-', '/')
        
        boy_chart = kundli_utils.get_chart(
            date_str=boy_date, time_str=details.boy_time, place=details.boy_place,
            zodiac=details.zodiac, house_system="Whole Sign",
            ayanamsa=details.ayanamsa, node_type=details.node_type
        )
        girl_chart = kundli_utils.get_chart(
            date_str=girl_date, time_str=details.girl_time, place=details.girl_place,
            zodiac=details.zodiac, house_system="Whole Sign",
            ayanamsa=details.ayanamsa, node_type=details.node_type
        )
        
        boy_moon_lon = boy_chart.get('Moon').lon
        girl_moon_lon = girl_chart.get('Moon').lon
        boy_planets = kundli_utils.get_planet_positions(boy_chart)
        girl_planets = kundli_utils.get_planet_positions(girl_chart)
        boy_rashi = boy_planets['Moon']['sign']
        girl_rashi = girl_planets['Moon']['sign']
        
        milan = kundli_utils.get_milan_score(boy_moon_lon, girl_moon_lon, boy_rashi, girl_rashi)
        
        return {
            "status": "success",
            "boy": {"nakshatra": milan['boy_nakshatra'], "rashi": milan['boy_rashi']},
            "girl": {"nakshatra": milan['girl_nakshatra'], "rashi": milan['girl_rashi']},
            "milan": milan
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
                "regional": regional_panchang,
                "d1_chart": kundli_utils.get_planet_positions(chart)
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
                # Compute divisional degree
                sign_lon = p_obj.lon % 30
                div_size = 30.0 / div
                rem = sign_lon % div_size
                div_lon = round(rem * div, 2)
                div_charts[f"D{div}"][p_name] = {
                    "sign": kundli_utils.get_divisional_chart_sign(p_obj.lon, div),
                    "lon": div_lon
                }
            asc_obj = chart.get('Asc')
            sign_lon = asc_obj.lon % 30
            div_size = 30.0 / div
            rem = sign_lon % div_size
            div_lon = round(rem * div, 2)
            div_charts[f"D{div}"]['Asc'] = {
                "sign": kundli_utils.get_divisional_chart_sign(asc_obj.lon, div),
                "lon": div_lon
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


if os.environ.get('VERCEL') or os.path.exists("/tmp"):
    VISITOR_FILE = "/tmp/visitors.json"
else:
    VISITOR_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visitors.json")

file_lock = threading.Lock()

from fastapi.responses import JSONResponse

@app.options("/api/visitor_count")
@app.post("/api/visitor_count")
@app.get("/api/visitor_count")
def get_visitor_count(request: Request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }
    try:
        ip = request.headers.get("x-forwarded-for")
        if ip:
            ip = ip.split(",")[0].strip()
        else:
            ip = request.client.host if (request and hasattr(request, 'client') and request.client) else "127.0.0.1"

        ip_hash = hashlib.sha256(ip.encode('utf-8')).hexdigest()
        now_str = datetime.now().isoformat()

        data = {"visits": {}, "total_visits": 1250, "unique_visitors": 480}
        is_repeat = False

        with file_lock:
            if os.path.exists(VISITOR_FILE):
                try:
                    with open(VISITOR_FILE, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        if isinstance(loaded, dict):
                            data = loaded
                except Exception as e:
                    print("Failed to load visitor file:", e)
            
            visits = data.setdefault("visits", {})
            if ip_hash in visits:
                visits[ip_hash]["count"] = visits[ip_hash].get("count", 0) + 1
                visits[ip_hash]["last_visit"] = now_str
                is_repeat = True
            else:
                visits[ip_hash] = {
                    "count": 1,
                    "first_visit": now_str,
                    "last_visit": now_str
                }
                data["unique_visitors"] = data.get("unique_visitors", 0) + 1
            
            data["total_visits"] = data.get("total_visits", 0) + 1

            try:
                os.makedirs(os.path.dirname(VISITOR_FILE), exist_ok=True)
                with open(VISITOR_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print("Failed to save visitor file:", e)

        return JSONResponse(
            content={
                "status": "success",
                "total_visits": data.get("total_visits", 1250),
                "unique_visitors": data.get("unique_visitors", 480),
                "is_repeat": is_repeat
            },
            headers=headers
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "success",
                "total_visits": 1250,
                "unique_visitors": 480,
                "is_repeat": True,
                "fallback": True
            },
            headers=headers
        )


import time

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

# ── FESTIVALS DATABASE & DYNAMIC SCANNER ──────────────────────────────────
import sqlite3

FESTIVAL_RULES = [
    # Ashadha
    { "name": "Ashadha Navratri Begins", "month": "Ashadha", "paksha": "Shukla", "tithi": "Pratipada", "icon": "🌸", "type": "Festival" },
    { "name": "Jagannath Rathyatra", "month": "Ashadha", "paksha": "Shukla", "tithi": "Dwitiya", "icon": "🚩", "type": "Festival" },
    { "name": "Skanda Sashti", "month": "Ashadha", "paksha": "Shukla", "tithi": "Shashthi", "icon": "🔱", "type": "Festival" },
    { "name": "Devshayani Ekadashi", "month": "Ashadha", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🛌", "type": "Vrat" },
    { "name": "Guru Purnima", "month": "Ashadha", "paksha": "Shukla", "tithi": "Purnima", "icon": "🎓", "type": "Festival" },
    { "name": "Yogini Ekadashi", "month": "Ashadha", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },

    # Shravana
    { "name": "Hariyali Teej", "month": "Shravana", "paksha": "Shukla", "tithi": "Tritiya", "icon": "🌿", "type": "Festival" },
    { "name": "Nag Panchami", "month": "Shravana", "paksha": "Shukla", "tithi": "Panchami", "icon": "🐍", "type": "Festival" },
    { "name": "Shravana Putrada Ekadashi", "month": "Shravana", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Varaha Jayanti", "month": "Shravana", "paksha": "Shukla", "tithi": "Dwadashi", "icon": "🐗", "type": "Festival" },
    { "name": "Raksha Bandhan", "month": "Shravana", "paksha": "Shukla", "tithi": "Purnima", "icon": "🤝", "type": "Festival" },
    { "name": "Kalki Jayanti", "month": "Shravana", "paksha": "Shukla", "tithi": "Shashthi", "icon": "🕉️", "type": "Festival" },
    { "name": "Kamika Ekadashi", "month": "Shravana", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },

    # Bhadrapada
    { "name": "Kajari Teej", "month": "Bhadrapada", "paksha": "Krishna", "tithi": "Tritiya", "icon": "🌿", "type": "Festival" },
    { "name": "Krishna Janmashtami", "month": "Bhadrapada", "paksha": "Krishna", "tithi": "Ashtami", "icon": "🍯", "type": "Festival" },
    { "name": "Aja Ekadashi", "month": "Bhadrapada", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Ganesha Chaturthi", "month": "Bhadrapada", "paksha": "Shukla", "tithi": "Chaturthi", "icon": "🐘", "type": "Festival" },
    { "name": "Radha Ashtami", "month": "Bhadrapada", "paksha": "Shukla", "tithi": "Ashtami", "icon": "🌸", "type": "Festival" },
    { "name": "Parsva Ekadashi", "month": "Bhadrapada", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Anant Chaturdashi", "month": "Bhadrapada", "paksha": "Shukla", "tithi": "Chaturdashi", "icon": "♾️", "type": "Festival" },

    # Ashwina
    { "name": "Indira Ekadashi", "month": "Ashwina", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Sarvapitri Amavasya", "month": "Ashwina", "paksha": "Krishna", "tithi": "Amavasya", "icon": "🕊️", "type": "Festival" },
    { "name": "Shardiya Navratri Begins", "month": "Ashwina", "paksha": "Shukla", "tithi": "Pratipada", "icon": "🔱", "type": "Festival" },
    { "name": "Saraswati Avahan", "month": "Ashwina", "paksha": "Shukla", "tithi": "Saptami", "icon": "📖", "type": "Festival" },
    { "name": "Durga Ashtami", "month": "Ashwina", "paksha": "Shukla", "tithi": "Ashtami", "icon": "🔱", "type": "Festival" },
    { "name": "Maha Navami", "month": "Ashwina", "paksha": "Shukla", "tithi": "Navami", "icon": "🏹", "type": "Festival" },
    { "name": "Dussehra", "month": "Ashwina", "paksha": "Shukla", "tithi": "Dashami", "icon": "🏹", "type": "Festival" },
    { "name": "Papankusha Ekadashi", "month": "Ashwina", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Kojagara Puja", "month": "Ashwina", "paksha": "Shukla", "tithi": "Purnima", "icon": "🌕", "type": "Festival" },

    # Kartika
    { "name": "Karwa Chauth", "month": "Kartika", "paksha": "Krishna", "tithi": "Chaturthi", "icon": "🌙", "type": "Vrat" },
    { "name": "Ahoi Ashtami", "month": "Kartika", "paksha": "Krishna", "tithi": "Ashtami", "icon": "👶", "type": "Vrat" },
    { "name": "Rama Ekadashi", "month": "Kartika", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Dhanteras", "month": "Kartika", "paksha": "Krishna", "tithi": "Trayodashi", "icon": "🪙", "type": "Festival" },
    { "name": "Narak Chaturdashi", "month": "Kartika", "paksha": "Krishna", "tithi": "Chaturdashi", "icon": "🪔", "type": "Festival" },
    { "name": "Diwali", "month": "Kartika", "paksha": "Krishna", "tithi": "Amavasya", "icon": "🪔", "type": "Festival" },
    { "name": "Govardhan Puja", "month": "Kartika", "paksha": "Shukla", "tithi": "Pratipada", "icon": "⛰️", "type": "Festival" },
    { "name": "Bhai Dooj", "month": "Kartika", "paksha": "Shukla", "tithi": "Dwitiya", "icon": "🌸", "type": "Festival" },
    { "name": "Chhath Puja", "month": "Kartika", "paksha": "Shukla", "tithi": "Shashthi", "icon": "☀️", "type": "Festival" },
    { "name": "Devutthana Ekadashi", "month": "Kartika", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔔", "type": "Vrat" },
    { "name": "Tulsi Vivah", "month": "Kartika", "paksha": "Shukla", "tithi": "Dwadashi", "icon": "🌿", "type": "Festival" },
    { "name": "Kartik Purnima", "month": "Kartika", "paksha": "Shukla", "tithi": "Purnima", "icon": "🌕", "type": "Festival" },

    # Margashirsha
    { "name": "Utpanna Ekadashi", "month": "Margashirsha", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Gita Jayanti", "month": "Margashirsha", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "📖", "type": "Festival" },
    { "name": "Dattatreya Jayanti", "month": "Margashirsha", "paksha": "Shukla", "tithi": "Purnima", "icon": "🕉️", "type": "Festival" },

    # Pausha
    { "name": "Saphala Ekadashi", "month": "Pausha", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Pausha Putrada Ekadashi", "month": "Pausha", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Shakambhari Purnima", "month": "Pausha", "paksha": "Shukla", "tithi": "Purnima", "icon": "🌕", "type": "Festival" },

    # Magha
    { "name": "Shattila Ekadashi", "month": "Magha", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Mauni Amavasya", "month": "Magha", "paksha": "Krishna", "tithi": "Amavasya", "icon": "🤫", "type": "Festival" },
    { "name": "Vasant Panchami", "month": "Magha", "paksha": "Shukla", "tithi": "Panchami", "icon": "🎻", "type": "Festival" },
    { "name": "Jaya Ekadashi", "month": "Magha", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Magha Purnima", "month": "Magha", "paksha": "Shukla", "tithi": "Purnima", "icon": "🌕", "type": "Festival" },

    # Phalguna
    { "name": "Vijaya Ekadashi", "month": "Phalguna", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Maha Shivaratri", "month": "Phalguna", "paksha": "Krishna", "tithi": "Chaturdashi", "icon": "🕉️", "type": "Festival" },
    { "name": "Amalaki Ekadashi", "month": "Phalguna", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Holika Dahan", "month": "Phalguna", "paksha": "Shukla", "tithi": "Chaturdashi", "icon": "🔥", "type": "Festival" },
    { "name": "Holi", "month": "Phalguna", "paksha": "Shukla", "tithi": "Purnima", "icon": "🎨", "type": "Festival" },

    # Chaitra
    { "name": "Papmochani Ekadashi", "month": "Chaitra", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Chaitra Navratri Begins", "month": "Chaitra", "paksha": "Shukla", "tithi": "Pratipada", "icon": "🔱", "type": "Festival" },
    { "name": "Gudi Padwa", "month": "Chaitra", "paksha": "Shukla", "tithi": "Pratipada", "icon": "🚩", "type": "Festival" },
    { "name": "Gangaur", "month": "Chaitra", "paksha": "Shukla", "tithi": "Tritiya", "icon": "🌸", "type": "Festival" },
    { "name": "Sri Rama Navami", "month": "Chaitra", "paksha": "Shukla", "tithi": "Navami", "icon": "🏹", "type": "Festival" },
    { "name": "Kamada Ekadashi", "month": "Chaitra", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Hanuman Jayanti", "month": "Chaitra", "paksha": "Shukla", "tithi": "Purnima", "icon": "🐒", "type": "Festival" },

    # Vaishakha
    { "name": "Varuthini Ekadashi", "month": "Vaishakha", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Akshaya Tritiya", "month": "Vaishakha", "paksha": "Shukla", "tithi": "Tritiya", "icon": "💎", "type": "Festival" },
    { "name": "Mohini Ekadashi", "month": "Vaishakha", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Narasimha Jayanti", "month": "Vaishakha", "paksha": "Shukla", "tithi": "Chaturdashi", "icon": "🦁", "type": "Festival" },
    { "name": "Buddha Purnima", "month": "Vaishakha", "paksha": "Shukla", "tithi": "Purnima", "icon": "🧘", "type": "Festival" },

    # Jyeshtha
    { "name": "Apara Ekadashi", "month": "Jyeshtha", "paksha": "Krishna", "tithi": "Ekadashi", "icon": "🔱", "type": "Vrat" },
    { "name": "Shani Jayanti", "month": "Jyeshtha", "paksha": "Krishna", "tithi": "Amavasya", "icon": "⚖️", "type": "Festival" },
    { "name": "Vat Savitri Vrat", "month": "Jyeshtha", "paksha": "Krishna", "tithi": "Amavasya", "icon": "🌳", "type": "Vrat" },
    { "name": "Ganga Dussehra", "month": "Jyeshtha", "paksha": "Shukla", "tithi": "Dashami", "icon": "🌊", "type": "Festival" },
    { "name": "Nirjala Ekadashi", "month": "Jyeshtha", "paksha": "Shukla", "tithi": "Ekadashi", "icon": "🏺", "type": "Vrat" },
    { "name": "Vat Purnima Vrat", "month": "Jyeshtha", "paksha": "Shukla", "tithi": "Purnima", "icon": "🌳", "type": "Vrat" },
]

RITUAL_RULES = [
    { "name": "Jagannath Yatra", "month": "Ashadha", "paksha": "Shukla", "tithi": "Dwitiya", "icon": "🚩", "type": "Festival" },
    { "name": "Shradh Karma Pitru Paksha Begins", "month": "Bhadrapada", "paksha": "Krishna", "tithi": "Pratipada", "icon": "🕊️", "type": "Festival" },
    { "name": "Kumbha Mela bathing day (Makar Sankranti)", "month": "Pausha", "paksha": "", "tithi": "", "icon": "🌊", "type": "Festival", "solar_sign": "Makara" },
]

def get_tithi_times(p):
    t_list = p.get('tithis_list', [])
    times_info = []
    if len(t_list) > 0:
        for idx, item in enumerate(t_list):
            name = item.get('name', '')
            end_time = item.get('end_time', '')
            start_time = "06:00" if idx == 0 else t_list[idx-1].get('end_time', '06:00')
            times_info.append({
                "name": name,
                "start": start_time,
                "end": end_time if end_time else "06:00 (Next Day)"
            })
    return times_info

def init_festivals_db():
    db_path = "/tmp/festivals.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS festivals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        name TEXT NOT NULL,
        classification TEXT NOT NULL,
        paksha TEXT,
        tithi TEXT,
        nakshatra TEXT,
        lunar_month TEXT,
        timing_details TEXT,
        icon TEXT
    )
    """)
    cursor.execute("SELECT COUNT(*) FROM festivals")
    if cursor.fetchone()[0] > 100:
        conn.close()
        return

    from datetime import datetime, timedelta
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2028, 12, 31)
    current = start_date

    while current <= end_date:
        date_str_slash = current.strftime("%Y/%m/%d")
        date_str_dash = current.strftime("%Y-%m-%d")
        
        try:
            chart = kundli_utils.get_chart(
                date_str=date_str_slash,
                time_str="12:00",
                place="New Delhi, India",
                zodiac="Sidereal",
                house_system="Whole Sign",
                ayanamsa="Lahiri",
                node_type="True"
            )
            sun_lon = chart.get('Sun').lon
            moon_lon = chart.get('Moon').lon
            
            panchang = kundli_utils.get_panchang(sun_lon, moon_lon, current.date(), chart.lat, chart.lon, chart.utc_offset_hours)
            panchang_ext = kundli_utils.get_extended_panchang(sun_lon, moon_lon, current.date(), chart.lat, chart.lon, chart.utc_offset_hours, chart.ayanamsa_val, chart.jd)
            
            sun_sign_idx = kundli_utils.SIGN_NAMES.index(kundli_utils.get_planet_positions(chart)['Sun']['sign'])
            lunar_month = kundli_utils.LUNAR_MONTHS[sun_sign_idx]
            sun_sign = kundli_utils.SIGN_NAMES[sun_sign_idx]
            
            tithi_at_noon = panchang.get('tithi', '')
            paksha = panchang_ext.get('paksha', 'Shukla')
            nakshatra = panchang.get('nakshatra', '')
            weekday = current.strftime("%A")
            
            t_times = get_tithi_times(panchang)
            
            def add_event(name, classification, timing, icon, tithi_name=None):
                cursor.execute("""
                INSERT INTO festivals (date, name, classification, paksha, tithi, nakshatra, lunar_month, timing_details, icon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (date_str_dash, name, classification, paksha, tithi_name or tithi_at_noon, nakshatra, lunar_month, timing, icon))

            # 1. Match rules
            for rule in FESTIVAL_RULES + RITUAL_RULES:
                m_match = not rule.get('month') or rule['month'].lower() in lunar_month.lower()
                p_match = not rule.get('paksha') or rule['paksha'].lower() in paksha.lower()
                t_match = not rule.get('tithi') or rule['tithi'].lower() in tithi_at_noon.lower()
                s_match = not rule.get('solar_sign') or rule['solar_sign'].lower() in sun_sign.lower()
                
                if m_match and p_match and t_match and s_match:
                    timing_str = "All day"
                    for t in t_times:
                        if rule.get('tithi') and rule['tithi'].lower() in t['name'].lower():
                            timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                            break
                    add_event(rule['name'], rule['type'], timing_str, rule['icon'], rule.get('tithi'))

            # 2. General Vrats
            if "Ekadashi" in tithi_at_noon:
                timing_str = "All day"
                for t in t_times:
                    if "Ekadashi" in t['name']:
                        timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                add_event("Ekadashi Vrat", "Vrat", timing_str, "🔱", "Ekadashi")
                
            if "Trayodashi" in tithi_at_noon:
                timing_str = "All day"
                for t in t_times:
                    if "Trayodashi" in t['name']:
                        timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                add_event("Pradosh Vrat", "Vrat", timing_str, "🔱", "Trayodashi")
                
            if "Chaturthi" in tithi_at_noon and paksha == "Krishna":
                timing_str = "All day"
                for t in t_times:
                    if "Chaturthi" in t['name']:
                        timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                add_event("Sankashti Chaturthi", "Vrat", f"Observed on Krishna Chaturthi. {timing_str}", "🕉️", "Chaturthi")

            if "Chaturthi" in tithi_at_noon and paksha == "Shukla":
                timing_str = "All day"
                for t in t_times:
                    if "Chaturthi" in t['name']:
                        timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                add_event("Vinayaka Chaturthi", "Vrat", timing_str, "🐘", "Chaturthi")

            if "Chaturdashi" in tithi_at_noon and paksha == "Krishna":
                timing_str = "All day"
                for t in t_times:
                    if "Chaturdashi" in t['name']:
                        timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                add_event("Masik Shivaratri", "Vrat", timing_str, "🔱", "Chaturdashi")

            if "Purnima" in tithi_at_noon:
                timing_str = "All day"
                for t in t_times:
                    if "Purnima" in t['name']:
                        timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                add_event("Purnima Vrat & Satyanarayan Puja", "Vrat", timing_str, "🌕", "Purnima")

            if "Amavasya" in tithi_at_noon:
                timing_str = "All day"
                for t in t_times:
                    if "Amavasya" in t['name']:
                        timing_str = f"Starts: {t['start']}, Ends: {t['end']}"
                add_event("Amavasya Vrat & Pitru Tarpan", "Vrat", timing_str, "🌑", "Amavasya")

            if "Pushya" in nakshatra:
                if weekday == "Thursday":
                    add_event("Gurupushyamrut Yoga", "Festival", "Auspicious planetary alignment for growth and learning", "⚡", "N/A")
                elif weekday == "Sunday":
                    add_event("Ravi Pushya Yoga", "Festival", "Highly auspicious alignment for purchasing metal and starting therapies", "☀️", "N/A")
        except Exception as ex:
            print(f"Skipping date {date_str_dash} due to error: {ex}")
            
        current += timedelta(days=1)
        
    conn.commit()
    conn.close()

# Start background DB initialization
def run_db_initializer():
    try:
        init_festivals_db()
    except Exception as e:
        print("Failed to initialize festivals db:", e)

threading.Thread(target=run_db_initializer, daemon=True).start()

class FestivalRequest(BaseModel):
    year: int = None
    month: int = None
    date: str = None

@app.post("/api/festivals")
def get_festivals_post(req: FestivalRequest):
    return query_festivals(req.year, req.month, req.date)

@app.get("/api/festivals")
def get_festivals_get(year: int = None, month: int = None, date: str = None):
    return query_festivals(year, month, date)

def query_festivals(year: int, month: int, date: str):
    db_path = "/tmp/festivals.db"
    if not os.path.exists(db_path):
        run_db_initializer()
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if date:
        date = date.replace('/', '-')
        cursor.execute("SELECT date, name, classification, paksha, tithi, nakshatra, lunar_month, timing_details, icon FROM festivals WHERE date=?", (date,))
    elif year and month:
        prefix = f"{year}-{month:02d}-%"
        cursor.execute("SELECT date, name, classification, paksha, tithi, nakshatra, lunar_month, timing_details, icon FROM festivals WHERE date LIKE ? ORDER BY date ASC", (prefix,))
    else:
        cursor.execute("SELECT date, name, classification, paksha, tithi, nakshatra, lunar_month, timing_details, icon FROM festivals ORDER BY date ASC")
        
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "date": r[0],
            "name": r[1],
            "classification": r[2],
            "paksha": r[3],
            "tithi": r[4],
            "nakshatra": r[5],
            "lunar_month": r[6],
            "timing_details": r[7],
            "icon": r[8]
        })
    return {"status": "success", "festivals": results}


