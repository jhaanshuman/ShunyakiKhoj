from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from datetime import datetime, date

# Append backend directory so we can import from kundli_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import kundli_utils

app = FastAPI(title="Vedic Astrology API", version="1.0.0")

# Enable CORS for frontend integration
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

@app.post("/api/calculate")
def calculate_chart(details: BirthDetails):
    try:
        # 1. Compute Chart
        chart = kundli_utils.get_chart(
            date_str=details.date,
            time_str=details.time,
            place=details.place,
            zodiac="Sidereal",
            house_system="Whole Sign",
            ayanamsa="Lahiri",
            node_type="True"
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
                "degree": asc_deg
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
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/dasha")
def calculate_dasha(details: BirthDetails):
    try:
        chart = kundli_utils.get_chart(
            date_str=details.date,
            time_str=details.time,
            place=details.place,
            zodiac="Sidereal",
            house_system="Whole Sign",
            ayanamsa="Lahiri",
            node_type="True"
        )
        moon_lon = chart.get('Moon').lon
        nak, lord, dasha_tree = kundli_utils.get_vimshottari_dasha(moon_lon, details.date)
        return {
            "status": "success",
            "moon_nakshatra": nak,
            "birth_lord": lord,
            "dasha_tree": dasha_tree
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class MatchDetails(BaseModel):
    boy_date: str
    boy_time: str
    boy_place: str
    girl_date: str
    girl_time: str
    girl_place: str


@app.post("/api/match")
def calculate_match(details: MatchDetails):
    try:
        # Calculate boy's chart
        boy_chart = kundli_utils.get_chart(
            date_str=details.boy_date,
            time_str=details.boy_time,
            place=details.boy_place,
            zodiac="Sidereal",
            house_system="Whole Sign",
            ayanamsa="Lahiri",
            node_type="True"
        )
        boy_moon_pos = kundli_utils.get_planet_positions(boy_chart)['Moon']
        boy_nak = boy_moon_pos['nakshatra']
        boy_sign = boy_moon_pos['sign']
        
        # Calculate girl's chart
        girl_chart = kundli_utils.get_chart(
            date_str=details.girl_date,
            time_str=details.girl_time,
            place=details.girl_place,
            zodiac="Sidereal",
            house_system="Whole Sign",
            ayanamsa="Lahiri",
            node_type="True"
        )
        girl_moon_pos = kundli_utils.get_planet_positions(girl_chart)['Moon']
        girl_nak = girl_moon_pos['nakshatra']
        girl_sign = girl_moon_pos['sign']
        
        # Calculate milan
        milan = kundli_utils.calculate_guna_milan(boy_nak, boy_sign, girl_nak, girl_sign)
        
        return {
            "status": "success",
            "boy": {"nakshatra": boy_nak, "rashi": boy_sign},
            "girl": {"nakshatra": girl_nak, "rashi": girl_sign},
            "milan": milan
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/health")
def health_check():
    return {"status": "ok"}

