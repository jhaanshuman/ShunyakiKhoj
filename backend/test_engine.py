# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from vedic_engine.master_horoscope import MasterHoroscopeBuilder
from database import EngineDatabase

def run_tests():
    print("=== 1. TESTING VEDIC ASTROLOGY CALCULATION ENGINE ===")
    master = MasterHoroscopeBuilder.build_master_horoscope(
        name="Test Native",
        gender="Male",
        dob_str="1994/01/05",
        tob_str="20:00",
        place="Patna, India",
        lat=25.5941,
        lon=85.1376,
        tz_offset=5.5,
        ayanamsa_name="Lahiri",
        node_type="True",
        house_system="Whole Sign"
    )
    print("[OK] Master Horoscope generated successfully!")
    print(f"[OK] Master Keys ({len(master.keys())}): {list(master.keys())}")
    print(f"[OK] Divisional Charts ({len(master['divisional_charts'])}): {list(master['divisional_charts'].keys())}")
    print(f"[OK] Special Points ({len(master['special_points'])}): {list(master['special_points'].keys())}")
    print(f"[OK] Arudha Padas ({len(master['arudhas'])}): {list(master['arudhas'].keys())}")
    print(f"[OK] Shadbala Planets ({len(master['shadbala'])}): {list(master['shadbala'].keys())}")
    print(f"[OK] Panchanga Tithi: {master['panchanga']['tithi_name']}")
    print(f"[OK] Active Yogas ({len(master['yogas'])}): {[y['name'] for y in master['yogas']]}")
    print(f"[OK] 5-Tier Vimshottari Mahadashas: {len(master['dasha']['vimshottari'])}")
    
    print("\n=== 2. TESTING SQLITE DATABASE SCHEMA & CACHING ===")
    EngineDatabase.initialize_schema()
    conn = EngineDatabase.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    print(f"[OK] SQLite Database Initialized! Total Tables ({len(tables)}): {tables}")
    
    # Save & Retrieve Cache
    hash_val = master['engine_metadata']['settings_hash']
    EngineDatabase.save_cached_horoscope(hash_val, master)
    cached = EngineDatabase.get_cached_horoscope(hash_val)
    assert cached is not None, "Cache retrieval failed!"
    print("[OK] Master Horoscope successfully cached and retrieved from SQLite DB!")
    
    print("\nALL VEDIC ASTROLOGY ENGINE & DATABASE VERIFICATIONS PASSED!")


if __name__ == "__main__":
    run_tests()
