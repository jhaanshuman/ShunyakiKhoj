# -*- coding: utf-8 -*-
"""
Database Persistence Layer: SQLite schema for caching, versioning, and AI data export.
"""
from datetime import datetime
import json
import os
import sqlite3
from typing import Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "astrology_engine.db")

ENGINE_VERSION = "2.2.0"
CALCULATION_VERSION = "1.0"

class EngineDatabase:
    """Manages SQLite tables and caches intermediate/master horoscope computations."""
    
    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def initialize_schema(cls):
        """Creates all 26 required SQLite tables with audit metadata."""
        conn = cls.get_connection()
        cursor = conn.cursor()

        audit_cols = """
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            engine_version TEXT NOT NULL,
            calculation_version TEXT NOT NULL,
            settings_hash TEXT NOT NULL
        """

        tables = [
            f"CREATE TABLE IF NOT EXISTS birth_profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_name TEXT, gender TEXT, dob TEXT, tob TEXT, place TEXT, lat REAL, lon REAL, tz_offset REAL, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS chart_settings (id INTEGER PRIMARY KEY AUTOINCREMENT, ayanamsa TEXT, node_type TEXT, house_system TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS planet_positions (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, planet_name TEXT, longitude REAL, latitude REAL, declination REAL, speed REAL, is_retro INTEGER, house INTEGER, sign TEXT, nakshatra TEXT, pada INTEGER, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS houses (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, house_number INTEGER, cusp_longitude REAL, sign TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS nakshatras (id INTEGER PRIMARY KEY AUTOINCREMENT, nakshatra_name TEXT, lord TEXT, start_deg REAL, end_deg REAL, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS panchanga (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, tithi TEXT, nakshatra TEXT, yoga TEXT, karana TEXT, vaara TEXT, rahu_kalam TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS upagrahas (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, upagraha_name TEXT, longitude REAL, house INTEGER, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS special_lagnas (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, lagna_name TEXT, longitude REAL, house INTEGER, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS arudhas (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, code TEXT, sign TEXT, house INTEGER, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS ashtakavarga (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, planet TEXT, bav_json TEXT, sav_json TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS shadbala (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, planet TEXT, total_virupas REAL, total_rupas REAL, ratio REAL, is_strong INTEGER, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS strengths (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, planet TEXT, ishta_phala REAL, kashta_phala REAL, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS yogas (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, yoga_name TEXT, category TEXT, formula TEXT, confidence REAL, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS dasha (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, dasha_type TEXT, mahadasha_lord TEXT, start_date TEXT, end_date TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS bhuktis (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, mahadasha TEXT, bhukti_lord TEXT, start_date TEXT, end_date TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS antar (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, bhukti TEXT, antar_lord TEXT, start_date TEXT, end_date TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS sookshma (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, antar TEXT, sookshma_lord TEXT, start_date TEXT, end_date TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS prana (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, sookshma TEXT, prana_lord TEXT, start_date TEXT, end_date TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS gochar (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, planet TEXT, transit_sign TEXT, house_from_moon INTEGER, is_benefic INTEGER, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT, description TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS prediction_rules (id INTEGER PRIMARY KEY AUTOINCREMENT, rule_name TEXT, condition_json TEXT, outcome_template TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS calculated_events (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, event_date TEXT, title TEXT, category TEXT, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS raw_astronomy (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, julian_day REAL, sidereal_time REAL, ayanamsa_val REAL, {audit_cols})",
            f"CREATE TABLE IF NOT EXISTS cache (settings_hash TEXT PRIMARY KEY, master_json TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)",
            f"CREATE TABLE IF NOT EXISTS AI_embeddings (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, embedding_vector TEXT, reasoning_graph_json TEXT, {audit_cols})",


            f"CREATE TABLE IF NOT EXISTS version_history (id INTEGER PRIMARY KEY AUTOINCREMENT, release_date TEXT, notes TEXT, {audit_cols})"

        ]

        for stmt in tables:
            cursor.execute(stmt)

        conn.commit()
        conn.close()

    @classmethod
    def get_cached_horoscope(cls, settings_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached Master Horoscope JSON by settings_hash."""
        cls.initialize_schema()
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT master_json FROM cache WHERE settings_hash = ?", (settings_hash,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row['master_json'])
        return None

    @classmethod
    def save_cached_horoscope(cls, settings_hash: str, master_obj: Dict[str, Any]):
        """Save Master Horoscope JSON object into cache."""
        cls.initialize_schema()
        conn = cls.get_connection()
        cursor = conn.cursor()
        now_str = datetime.utcnow().isoformat()
        master_json = json.dumps(master_obj)
        cursor.execute("""
            INSERT OR REPLACE INTO cache (settings_hash, master_json, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (settings_hash, master_json, now_str, now_str))
        conn.commit()
        conn.close()

