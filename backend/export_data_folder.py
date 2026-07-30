# -*- coding: utf-8 -*-
import sys
import os
import json

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'backend'))

from backend.vedic_engine.master_horoscope import MasterHoroscopeBuilder

def export_verification_data():
    data_dir = os.path.join(root_dir, 'Data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. Define Sample User Input Settings
    input_data = {
        "person_details": {
            "name": "Anshuman Jha",
            "gender": "Male",
            "date_of_birth": "1994/01/05",
            "time_of_birth": "20:00:00",
            "place_of_birth": "Patna, Bihar, India",
            "latitude": 25.5941,
            "longitude": 85.1376,
            "timezone_offset": 5.5,
            "daylight_saving": 0.0
        },
        "engine_settings": {
            "ayanamsa": "Lahiri",
            "node_type": "True",
            "house_system": "Whole Sign",
            "chart_style": "North",
            "rashi_visibility": "Visible",
            "outer_planets": "Visible",
            "terminology": "Vedic",
            "longitude_style": "Degrees-Minutes-Seconds",
            "zodiac_system": "Sidereal"
        }
    }
    
    input_file = os.path.join(data_dir, 'input_settings.json')
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(input_data, f, indent=2, ensure_ascii=False)
    print(f"Saved Input Settings to: {input_file}")
    
    # 2. Calculate Complete Master Horoscope Object
    master_output = MasterHoroscopeBuilder.build_master_horoscope(
        name=input_data["person_details"]["name"],
        gender=input_data["person_details"]["gender"],
        dob_str=input_data["person_details"]["date_of_birth"],
        tob_str=input_data["person_details"]["time_of_birth"],
        place=input_data["person_details"]["place_of_birth"],
        lat=input_data["person_details"]["latitude"],
        lon=input_data["person_details"]["longitude"],
        tz_offset=input_data["person_details"]["timezone_offset"],
        ayanamsa_name=input_data["engine_settings"]["ayanamsa"],
        node_type=input_data["engine_settings"]["node_type"],
        house_system=input_data["engine_settings"]["house_system"]
    )
    
    master_output["status"] = "success"
    
    output_file = os.path.join(data_dir, 'output_master_horoscope.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(master_output, f, indent=2, ensure_ascii=False)
    print(f"Saved Complete Master Output JSON to: {output_file}")
    print(f"Master Output contains {len(master_output)} root keys:")
    for k in master_output.keys():
        print(f"  - {k}")

if __name__ == "__main__":
    export_verification_data()
