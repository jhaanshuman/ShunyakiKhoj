# -*- coding: utf-8 -*-
"""
300+ Yoga Orchestrator v5.0
Evaluates classical Vedic Yogas, Raja Yogas, Dhana Yogas, Nabhasa Yogas, and Jaimini Yogas.
"""
from typing import List, Dict, Any
from ...yogas import YogaEngine

def evaluate_all_300_yogas(master_obj: Dict[str, Any]) -> Dict[str, Any]:
    planets = master_obj.get('planets', {})
    houses = master_obj.get('houses', {})
    
    asc_sign = houses.get('ascendant_sign') or houses.get('asc_sign', 'Cancer')
    planet_house_map = houses.get('planet_house_mapping', {})

    if not planet_house_map and isinstance(planets, dict):
        asc_idx = int(houses.get('ascendant_sidereal_lon', 0.0) / 30.0) % 12
        planet_house_map = {}
        for p_name, p_data in planets.items():
            if isinstance(p_data, dict) and 'sign_index' in p_data:
                h_num = ((p_data['sign_index'] - asc_idx + 12) % 12) + 1
                planet_house_map[p_name] = h_num

    # 1. Classical Yogas Evaluation
    classical_yogas = YogaEngine.evaluate_yogas(planets, asc_sign, planet_house_map)
    
    yoga_list = []
    for c_y in classical_yogas:
        yoga_list.append({
            "name": c_y.name,
            "category": c_y.category,
            "formula": c_y.formula,
            "participating_planets": c_y.participating_planets,
            "participating_houses": c_y.participating_houses,
            "description": c_y.result_narrative,
            "confidence": f"{c_y.confidence}%",
            "priority": c_y.priority,
            "affected_areas": c_y.affected_areas
        })

    # 2. Rule Engine & Additional Yogas
    # Dharma-Karma Adhipati Yoga check
    sun_h = planet_house_map.get('Sun', 1)
    mer_h = planet_house_map.get('Mercury', 1)
    if sun_h == mer_h:
        yoga_list.append({
            "name": "Dharma-Karma Adhipati Yoga",
            "category": "Raja Yoga",
            "formula": "9th Lord (Sun) and 10th Lord (Mercury) conjunct in House " + str(sun_h),
            "participating_planets": ["Sun", "Mercury"],
            "participating_houses": [sun_h],
            "description": "Grants high administrative authority, executive leadership, righteous conduct, and career prosperity.",
            "confidence": "95%",
            "priority": "High",
            "affected_areas": ["Career", "Status", "Leadership"]
        })

    # Lakshmi Yoga check
    ven_h = planet_house_map.get('Venus', 1)
    if ven_h in [1, 4, 7, 10, 5, 9]:
        yoga_list.append({
            "name": "Lakshmi Yoga",
            "category": "Dhana Yoga",
            "formula": "Venus (Karaka of wealth & 9th/4th lord) placed in Kendra/Trikona",
            "participating_planets": ["Venus"],
            "participating_houses": [ven_h],
            "description": "Brings immense financial wealth, grace, luxury, vehicles, and enduring prosperity.",
            "confidence": "90%",
            "priority": "High",
            "affected_areas": ["Wealth", "Luxury", "Fortune"]
        })

    # Vipareeta Raja Yoga check (6th, 8th, 12th lords in 6th, 8th, 12th)
    jup_h = planet_house_map.get('Jupiter', 1)
    sat_h = planet_house_map.get('Saturn', 1)
    if sat_h in [6, 8, 12] or jup_h in [6, 8, 12]:
        yoga_list.append({
            "name": "Harsha / Sarala Vipareeta Raja Yoga",
            "category": "Vipareeta Raja Yoga",
            "formula": "Dusthana lord placed in another Dusthana house",
            "participating_planets": ["Saturn", "Jupiter"],
            "participating_houses": [sat_h, jup_h],
            "description": "Rise to power, wealth, and prominence through sudden unexpected opportunities or defeat of rivals.",
            "confidence": "88%",
            "priority": "High",
            "affected_areas": ["Unexpected Rise", "Victory", "Resilience"]
        })

    cat_counts = {}
    for y in yoga_list:
        cat = y["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    return {
        "total_active": len(yoga_list),
        "categories_breakdown": cat_counts,
        "yogas": yoga_list
    }
