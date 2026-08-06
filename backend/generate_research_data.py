# -*- coding: utf-8 -*-
"""
generate_research_data.py
Executes the single canonical V5.0 Master Horoscope Builder for the benchmark profile:
Name: Anshuman Kumar Jha
DOB: 1994/01/05
TOB: 20:00
POB: Patna, Bihar

Generates single source of truth `master.json`, `graphs.json`, `tables.json`,
and aligned domain-specific JSON files.
"""

import sys
import os
import json

backend_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(backend_dir)
sys.path.insert(0, root_dir)
sys.path.append(backend_dir)

from vedic_engine.orchestrator.master_builder_v5 import MasterHoroscopeBuilderV5
import api.kundli_utils as kundli_utils
import api.calculate as calc_module

def main():
    input_path = os.path.join(backend_dir, "input", "anshuman_jha_input.json")
    output_dir = os.path.join(backend_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Reading input profile from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    profile = input_data["user_profile"]
    opts = input_data["calculation_options"]

    print("Computing Single Canonical Master Horoscope V5.0 for Anshuman Kumar Jha...")
    master_obj = MasterHoroscopeBuilderV5.build_master_horoscope(
        name=profile["name"],
        gender=profile["gender"],
        dob_str=profile["dob"],
        tob_str=profile["tob"],
        place=profile["pob"],
        lat=profile["latitude"],
        lon=profile["longitude"],
        tz_offset=profile["tz_offset"],
        ayanamsa_name=opts.get("ayanamsa", "Lahiri"),
        node_type=opts.get("node_type", "True"),
        house_system=opts.get("house_system", "Whole Sign"),
        requested_modules=["ALL"]
    )

    # Attach input metadata into master object
    master_obj["benchmark_input"] = input_data

    # Generate flat D1 chart for backward compatibility
    asc_sign_idx = int(master_obj['houses']['ascendant_sidereal_lon'] / 30.0) % 12
    d1_flat = {}
    for p_name, p_data in master_obj.get('planets', {}).items():
        if isinstance(p_data, dict):
            h_num = p_data.get('house', ((p_data.get('sign_index', 0) - asc_sign_idx + 12) % 12) + 1)
            d1_flat[p_name] = {
                'sign': p_data.get('sign_name', ''),
                'degree': p_data.get('sign_degree', 0.0),
                'longitude': p_data.get('sidereal_lon', 0.0),
                'nakshatra': p_data.get('nakshatra_name', ''),
                'pada': p_data.get('pada', 1),
                'house': h_num,
                'is_retrograde': p_data.get('is_retrograde', False),
                'is_combust': p_data.get('is_combust', False)
            }
    master_obj['d1_chart'] = d1_flat

    # 1. Primary Canonical Output File: master.json
    master_json_path = os.path.join(output_dir, "master.json")
    anshuman_json_path = os.path.join(output_dir, "anshuman_jha_output.json")

    def safe_serialize(obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        if isinstance(obj, set):
            return list(obj)
        return str(obj)

    with open(master_json_path, "w", encoding="utf-8") as f:
        json.dump(master_obj, f, indent=2, ensure_ascii=False, default=safe_serialize)
    print(f"Saved primary canonical output to {master_json_path}")

    with open(anshuman_json_path, "w", encoding="utf-8") as f:
        json.dump(master_obj, f, indent=2, ensure_ascii=False, default=safe_serialize)
    print(f"Saved primary research output to {anshuman_json_path}")

    # 2. Extract Specialized System Outputs
    graphs_data = master_obj.get("house_graph", {})
    tables_data = {
        "planets": master_obj.get("planets", {}),
        "houses": master_obj.get("houses", {}),
        "shadbala": master_obj.get("shadbala", {}),
        "ashtakavarga": master_obj.get("ashtakavarga", {}),
        "dasha": master_obj.get("dasha", {})
    }

    with open(os.path.join(output_dir, "graphs.json"), "w", encoding="utf-8") as f:
        json.dump(graphs_data, f, indent=2, ensure_ascii=False, default=safe_serialize)
    with open(os.path.join(output_dir, "tables.json"), "w", encoding="utf-8") as f:
        json.dump(tables_data, f, indent=2, ensure_ascii=False, default=safe_serialize)

    # 3. Categorical Domain Outlets for Research Portal
    domain_files = {
        "horoscope_summary.json": master_obj.get("houses", {}),
        "planets_dignities.json": master_obj.get("planets", {}),
        "divisional_charts.json": master_obj.get("divisional_charts", {}),
        "dasha_systems.json": master_obj.get("dasha", {}),
        "panchang_astronomy.json": master_obj.get("panchanga", {}),
        "ashtakvarga_points.json": master_obj.get("ashtakavarga", {}),
        "yogas_and_doshas.json": {"yogas": master_obj.get("yogas", []), "doshas": master_obj.get("dosha_result", {})},
        "shadbala_ishta_kashta.json": master_obj.get("shadbala", {}),
        "arudha_upagraha_lagnas.json": {"arudha_lagnas": master_obj.get("arudhas", {}), "special_points": master_obj.get("special_points", {})},
        "jaimini_engine.json": master_obj.get("jaimini", {}),
        "house_planet_strengths_avasthas.json": {"house_analysis": master_obj.get("house_analysis", {}), "planet_state": master_obj.get("planet_state", {})},
        "all_evaluated_yogas.json": master_obj.get("yogas", []),
        "all_evaluated_doshas.json": master_obj.get("dosha_result", {}),
        "aspects_argala_bhavatbhavam.json": {"planetary_aspects": master_obj.get("planetary_aspects", {}), "arudhas": master_obj.get("arudhas", {})},
        "kp_engine_expanded.json": master_obj.get("kp", {}),
        "advanced_marriage_synastry.json": master_obj.get("matching", {}),
        "event_prediction_windows.json": master_obj.get("event_indicators", {}),
        "dasha_interpretations.json": master_obj.get("dasha", {}),
        "ai_reasoning_synthesis.json": master_obj.get("ai_context", {})
    }

    for fname, data in domain_files.items():
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=safe_serialize)
        print(f"Saved domain output {fname}")

    print("SUCCESS: Unified Master Engine & Refactored Data Generation Complete!")

if __name__ == "__main__":
    main()
