# -*- coding: utf-8 -*-
"""
ShunyaKiKhoj BPHS & PhalaDeepika Rule Database Ingestor
Parses BPHS_Vol1_Rule_Database.xlsx and generates bphs_rule_base.json
containing 1,558 source rules, 2,601 atomic conditions, and 101 named yogas.
"""

import os
import json
import pandas as pd

def ingest_rule_database():
    excel_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "RuleBase", "BPHS_Vol1_Rule_Database.xlsx")
    excel_path = os.path.abspath(excel_path)
    output_json = os.path.join(os.path.dirname(__file__), "bphs_rule_base.json")
    output_json = os.path.abspath(output_json)

    print(f"Ingesting BPHS Rule Database from: {excel_path}")

    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found.")
        return

    # Read Rule_Master
    df_master = pd.read_excel(excel_path, sheet_name='Rule_Master').fillna('')
    # Read Rule_Conditions
    df_conds = pd.read_excel(excel_path, sheet_name='Rule_Conditions').fillna('')
    # Read Yoga_Catalog
    df_yogas = pd.read_excel(excel_path, sheet_name='Yoga_Catalog').fillna('')

    # Group conditions by Rule_ID
    conds_by_rule = {}
    for idx, row in df_conds.iterrows():
        r_id = str(row.get('Rule_ID', '')).strip()
        if not r_id:
            continue
        if r_id not in conds_by_rule:
            conds_by_rule[r_id] = []
        conds_by_rule[r_id].append({
            "atom_no": row.get('Atom_No', ''),
            "entity": row.get('Entity/Planet', ''),
            "relation_type": row.get('Relation_Type', ''),
            "relation_value": row.get('Relation_Value', ''),
            "lord_house": row.get('Lord_House', ''),
            "target_house": row.get('Target_House', ''),
            "condition_text": row.get('Condition_Text', ''),
            "source_locator": row.get('Source_Locator', '')
        })

    # Group yogas by Rule_ID
    yogas_list = []
    for idx, row in df_yogas.iterrows():
        yogas_list.append({
            "yoga_name": str(row.get('Yoga_Name', '')),
            "rule_id": str(row.get('Rule_ID', '')),
            "chapter": str(row.get('Chapter', '')),
            "verse_no": str(row.get('Verse_No', '')),
            "formation_or_effect": str(row.get('Formation_or_Effect', ''))
        })

    rules_dict = {}
    for idx, row in df_master.iterrows():
        r_id = str(row.get('Rule_ID', '')).strip()
        if not r_id:
            continue
        rules_dict[r_id] = {
            "rule_id": r_id,
            "volume": str(row.get('Volume', '')),
            "chapter": str(row.get('Chapter', '')),
            "chapter_title": str(row.get('Chapter_Title', '')),
            "verse_no": str(row.get('Verse_No', '')),
            "rule_class": str(row.get('Rule_Class', '')),
            "event_category": str(row.get('Event_Category', '')),
            "subject_planets": str(row.get('Subject_Planets', '')),
            "reference_point": str(row.get('Reference_Point', '')),
            "relation_type": str(row.get('Relation_Type', '')),
            "lord_house": str(row.get('Lord_House', '')),
            "target_house": str(row.get('Target_House', '')),
            "condition_text": str(row.get('Condition_Text', '')),
            "outcome_text": str(row.get('Outcome_Text', '')),
            "polarity": str(row.get('Polarity', '')),
            "source_rule_text": str(row.get('Source_Rule_Text', '')),
            "atomic_conditions": conds_by_rule.get(r_id, [])
        }

    dataset = {
        "metadata": {
            "title": "BPHS & PhalaDeepika Master Rule Database",
            "total_rules": len(rules_dict),
            "total_conditions": len(df_conds),
            "total_yogas": len(yogas_list)
        },
        "rules": rules_dict,
        "yogas": yogas_list
    }

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Successfully ingested {len(rules_dict):,} rules and {len(df_conds):,} conditions into {output_json}!")

if __name__ == '__main__':
    ingest_rule_database()
