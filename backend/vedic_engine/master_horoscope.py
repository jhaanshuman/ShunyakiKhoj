# -*- coding: utf-8 -*-
"""
Master Horoscope Engine: Orchestrates all sub-engines to build the Master Horoscope Object.
Version 4.0.0 — Deterministic Reasoning Platform with full evidence chains,
planet state dimensions, house dependency graph, domain synthesis, and AI context.
"""
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import json
from typing import Dict, Any, Optional

# ── Core Calculation Engines ───────────────────────────────────────────────────
from .astronomy import AstronomyEngine, AstronomicalData
from .planets import PlanetEngine, PlanetPosition
from .houses import HouseEngine, HouseSystemData
from .divisional import DivisionalEngine
from .special_points import SpecialPointsEngine
from .arudhas import ArudhaEngine
from .strengths import StrengthEngine
from .ashtakavarga import AshtakavargaEngine
from .dashas import DashaEngine
from .yogas import YogaEngine
from .panchanga import PanchangaEngine
from .transits import TransitEngine

# ── Enterprise Rule & Prediction Engines (Phases 1–11) ────────────────────────
from .validation_engine import ValidationEngine
from .aspect_engine import AspectEngine
from .conjunction_engine import ConjunctionEngine
from .dignity_engine import DignityEngine
from .house_analysis_engine import HouseAnalysisEngine
from .functional_planet_engine import FunctionalPlanetEngine
from .planet_ranking_engine import PlanetRankingEngine
from .advanced_yoga_engine import AdvancedYogaEngine
from .rule_engine import RuleEngine
from .event_indicator_engine import EventIndicatorEngine
from .prediction_index_engine import PredictionIndexEngine

# ── v4.0 Reasoning Engines (Phases 12–18) ─────────────────────────────────────
from .planet_state_engine import PlanetStateEngine
from .planet_influence_network import PlanetInfluenceNetwork
from .house_graph_engine import HouseGraphEngine
from .evidence_engine import EvidenceEngine
from .domain_synthesis_engine import DomainSynthesisEngine
from .timeline_engine import TimelineEngine
from .ai_context_engine import AIContextEngine

ENGINE_VERSIONS = {
    "core": "2.2.0",
    "rule_engine": "3.0.0",
    "validation_engine": "1.0.0",
    "aspect_engine": "2.0.0",
    "conjunction_engine": "2.0.0",
    "dignity_engine": "2.0.0",
    "house_analysis_engine": "2.0.0",
    "functional_planet_engine": "1.0.0",
    "planet_ranking_engine": "1.0.0",
    "advanced_yoga_engine": "3.0.0",
    "event_indicator_engine": "1.0.0",
    "prediction_index_engine": "2.0.0",
    # v4.0 engines
    "planet_state_engine": "1.0.0",
    "planet_influence_network": "1.0.0",
    "house_graph_engine": "1.0.0",
    "evidence_engine": "1.0.0",
    "domain_synthesis_engine": "1.0.0",
    "timeline_engine": "1.0.0",
    "ai_context_engine": "1.0.0"
}

class MasterHoroscopeBuilder:
    """Single point of entry for building complete, synchronized Master Horoscope Objects (v4.0)."""
    
    @classmethod
    def build_master_horoscope(
        cls,
        name: str,
        gender: str,
        dob_str: str,  # YYYY/MM/DD or YYYY-MM-DD
        tob_str: str,  # HH:MM
        place: str,
        lat: float,
        lon: float,
        tz_offset: float = 5.5,
        ayanamsa_name: str = "Lahiri",
        node_type: str = "True",
        house_system: str = "Whole Sign",
        custom_ayanamsa_offset: float = 0.0
    ) -> Dict[str, Any]:
        """Compute and assemble the complete Master Horoscope Object."""
        # 1. Parse Datetime (Local to UT)
        clean_dob = dob_str.replace('-', '/')
        dob_parts = [int(x) for x in clean_dob.split('/')]
        tob_parts = [int(x) for x in tob_str.split(':')]
        
        local_dt = datetime(dob_parts[0], dob_parts[1], dob_parts[2], tob_parts[0], tob_parts[1])
        ut_dt = local_dt - timedelta(hours=tz_offset) if 'timedelta' in globals() else local_dt
        # Simple UT conversion
        total_seconds_offset = int(tz_offset * 3600)
        import datetime as dt_module
        ut_dt = local_dt - dt_module.timedelta(seconds=total_seconds_offset)

        # Settings Hash for caching & recalculation tracking
        settings_str = f"{dob_str}_{tob_str}_{lat:.4f}_{lon:.4f}_{tz_offset}_{ayanamsa_name}_{node_type}_{house_system}_{custom_ayanamsa_offset}"
        settings_hash = hashlib.sha256(settings_str.encode('utf-8')).hexdigest()[:16]

        # 2. Astronomy Engine
        astro_data = AstronomyEngine.calculate_astronomy_data(
            dt_ut=ut_dt,
            lat=lat,
            lon=lon,
            ayanamsa_name=ayanamsa_name,
            custom_ayanamsa_offset=custom_ayanamsa_offset
        )

        # 3. Planet Engine
        planets_data = PlanetEngine.calculate_planets(
            jd_ut=astro_data.julian_day_ut,
            ayanamsa_val=astro_data.ayanamsa_val,
            node_type=node_type
        )

        # 4. House Engine
        house_data = HouseEngine.calculate_houses(
            jd_ut=astro_data.julian_day_ut,
            lat=lat,
            lon=lon,
            ayanamsa_val=astro_data.ayanamsa_val,
            system_name=house_system,
            planets_data=planets_data
        )

        # 5. Divisional Engine (D1 to D144)
        div_charts = DivisionalEngine.calculate_all_divisional_charts(
            asc_sid_lon=house_data.ascendant_sidereal_lon,
            planets_data=planets_data
        )

        # 6. Special Points & Lagnas Engine
        sun_lon = planets_data['Sun'].sidereal_lon
        moon_lon = planets_data['Moon'].sidereal_lon
        rahu_lon = planets_data['Rahu'].sidereal_lon
        mars_lon = planets_data['Mars'].sidereal_lon
        jup_lon = planets_data['Jupiter'].sidereal_lon
        ven_lon = planets_data['Venus'].sidereal_lon
        
        special_points = SpecialPointsEngine.calculate_special_points(
            asc_sid_lon=house_data.ascendant_sidereal_lon,
            sun_sid_lon=sun_lon,
            moon_sid_lon=moon_lon,
            rahu_sid_lon=rahu_lon,
            mars_sid_lon=mars_lon,
            jupiter_sid_lon=jup_lon,
            venus_sid_lon=ven_lon,
            sunrise_jd=astro_data.sunrise_ut or astro_data.julian_day_ut,
            birth_jd=astro_data.julian_day_ut
        )

        # 7. Arudhas Engine
        arudhas = ArudhaEngine.calculate_arudhas(
            asc_sign_name=house_data.ascendant_sign,
            planets_data=planets_data
        )

        # 8. Strength Engine (Shadbala & Ishta/Kashta)
        is_day = 6.0 <= local_dt.hour < 18.0
        shadbala_data = StrengthEngine.calculate_shadbala(
            planets_data=planets_data,
            asc_sid_lon=house_data.ascendant_sidereal_lon,
            is_day_birth=is_day
        )
        ishta_kashta = StrengthEngine.calculate_ishta_kashta(shadbala_data, planets_data)

        # 9. Ashtakavarga Engine
        ashtakavarga = AshtakavargaEngine.calculate_bav_and_sav(
            planets_data=planets_data,
            asc_sid_lon=house_data.ascendant_sidereal_lon
        )

        # 10. Dasha Engine (5-tier Vimshottari & Yogini)
        vimshottari = DashaEngine.calculate_vimshottari(
            moon_sid_lon=moon_lon,
            birth_dt=local_dt,
            depth=5
        )
        yogini = DashaEngine.calculate_yogini(
            moon_sid_lon=moon_lon,
            birth_dt=local_dt
        )

        # 11. Panchanga Engine
        panchanga = PanchangaEngine.calculate_panchanga(
            sun_sid_lon=sun_lon,
            moon_sid_lon=moon_lon,
            birth_dt=local_dt,
            sunrise_jd=astro_data.sunrise_ut,
            sunset_jd=astro_data.sunset_ut
        )

        # 12. Yoga Engine
        yogas = YogaEngine.evaluate_yogas(
            planets_data=planets_data,
            asc_sign_name=house_data.ascendant_sign,
            planet_house_map=house_data.planet_house_mapping
        )

        # 13. Real-time Transits
        moon_sign_idx = int((moon_lon % 360.0) // 30)
        asc_sign_idx = int((house_data.ascendant_sidereal_lon % 360.0) // 30)
        transits_raw = TransitEngine.calculate_gochar(
            natal_moon_sign_idx=moon_sign_idx,
            natal_asc_sign_idx=asc_sign_idx,
            transit_planets_data=planets_data
        )
        transits_clean = {
            "transits": {k: asdict(v) for k, v in transits_raw['transits'].items()},
            "sade_sati": transits_raw['sade_sati']
        }


        # 14. Structured AI Graph Layer Export
        ai_graph = {
            "entity": name,
            "ascendant": house_data.ascendant_sign,
            "moon_sign": planets_data['Moon'].sign_name,
            "sun_sign": planets_data['Sun'].sign_name,
            "nakshatra": planets_data['Moon'].nakshatra_name,
            "current_mahadasha": vimshottari[0]['lord'] if vimshottari else None,
            "active_yogas": [y.name for y in yogas],
            "shadbala_strongest": max(shadbala_data.items(), key=lambda x: x[1].ratio)[0] if shadbala_data else None,
            "sade_sati_active": transits_clean['sade_sati']['is_active']

        }

        # ── Phase 0: Serialize core planet data for downstream engines ──────────────
        planets_dict = {p_name: asdict(p_obj) for p_name, p_obj in planets_data.items()}
        shadbala_dict = {k: asdict(v) for k, v in shadbala_data.items()}
        # Shadbala as plain virupas float for ranking/analysis engines
        shadbala_virupas = {p: v.total_virupas for p, v in shadbala_data.items()}

        # ── Phase 4: Complete Dignity Engine ─────────────────────────────────────────
        dignity_result = DignityEngine.calculate_complete_dignities(planets_dict)

        # ── Phase 2: Planetary Aspect Engine ─────────────────────────────────────────
        aspect_result = AspectEngine.calculate_aspects(planets_dict, asc_sign_idx)

        # ── Phase 3: Conjunction Engine ───────────────────────────────────────────────
        conjunction_result = ConjunctionEngine.calculate_conjunctions(planets_dict)

        # ── Assemble partial master_obj for downstream engines ────────────────────────
        partial_obj = {
            "planets": planets_dict,
            "houses": asdict(house_data),
            "shadbala": shadbala_virupas,
            "dignity": dignity_result,
            "planetary_aspects": aspect_result["planetary_aspects"],
            "yogas": [asdict(y) for y in yogas],
            "ashtakavarga": ashtakavarga
        }

        # ── Phase 5: House Analysis Engine ───────────────────────────────────────────
        house_analysis = HouseAnalysisEngine.analyze_houses(partial_obj)
        partial_obj['house_analysis'] = house_analysis

        # ── Phase 6: Functional Planet Classification ─────────────────────────────────
        functional_class = FunctionalPlanetEngine.classify_planets(asc_sign_idx)
        partial_obj['functional_classification'] = functional_class

        # ── Phase 7: Planet Strength Ranking ─────────────────────────────────────────
        planet_ranking = PlanetRankingEngine.rank_planets(partial_obj)
        partial_obj['planet_ranking'] = planet_ranking

        # ── Phase 8: Advanced Yoga Engine ────────────────────────────────────────────
        advanced_yogas = AdvancedYogaEngine.detect_all_yogas(partial_obj)

        # ── Phase 9: Deterministic Rule Engine ───────────────────────────────────────
        # Merge yoga data (classical + advanced) for rule matching
        all_yoga_dicts = [asdict(y) for y in yogas] + advanced_yogas
        partial_obj['yogas'] = all_yoga_dicts
        rule_matches = RuleEngine.evaluate_rules(partial_obj)
        partial_obj['rule_matches'] = rule_matches

        # ── Phase 10: Event Indicator Engine ──────────────────────────────────────────
        event_indicators = EventIndicatorEngine.calculate_event_indicators(partial_obj)
        partial_obj['event_indicators'] = event_indicators

        # ── Phase 11: Prediction Index Engine ────────────────────────────────────────
        prediction_index = PredictionIndexEngine.generate_prediction_index(partial_obj)

        # ── Phase 1: Validation Engine (runs after full assembly) ─────────────────────
        # Build temporary master for validation
        validation_target = {
            "engine_metadata": {"version": "3.0.0"},
            "birth_data": {"name": name},
            "astronomical_data": asdict(astro_data),
            "planets": planets_dict,
            "houses": asdict(house_data),
            "divisional_charts": div_charts,
            "special_points": {k: asdict(v) for k, v in special_points.items()},
            "arudhas": {k: asdict(v) for k, v in arudhas.items()},
            "shadbala": shadbala_dict,
            "ashtakavarga": ashtakavarga,
            "dasha": {"vimshottari": vimshottari},
            "panchanga": asdict(panchanga)
        }
        validation_result = ValidationEngine.validate_horoscope(validation_target)

        birth_data_dict = {
            "name": name,
            "gender": gender,
            "date_of_birth": dob_str,
            "birth_date": dob_str,  # alias for timeline engine
            "birth_time": tob_str,
            "time_of_birth": tob_str,
            "place": place,
            "latitude": lat,
            "longitude": lon,
            "timezone_offset": tz_offset,
            "ayanamsa_name": ayanamsa_name,
            "node_type": node_type,
            "house_system": house_system
        }

        # ── Phase 12: Planet State Engine ────────────────────────────────
        partial_obj['birth_data'] = birth_data_dict
        partial_obj['dasha'] = {"vimshottari": vimshottari, "yogini": yogini}
        partial_obj['transits'] = transits_clean
        planet_state = PlanetStateEngine.compute(partial_obj)
        partial_obj['planet_state'] = planet_state

        # ── Phase 13: Planet Influence Network ───────────────────────────
        planet_network = PlanetInfluenceNetwork.build(partial_obj)
        partial_obj['planet_influence_network'] = planet_network

        # ── Phase 14: House Graph Engine ─────────────────────────────────
        house_graph = HouseGraphEngine.build(partial_obj)
        partial_obj['house_graph'] = house_graph

        # ── Phase 15: Evidence Registry ──────────────────────────────────
        evidence_registry = EvidenceEngine.compile(partial_obj)
        partial_obj['evidence_registry'] = evidence_registry

        # ── Phase 16: Domain Synthesis Engine ────────────────────────────
        domain_synthesis = DomainSynthesisEngine.synthesize(partial_obj)
        partial_obj['domain_synthesis'] = domain_synthesis

        # ── Phase 17: Timeline Engine ─────────────────────────────────────
        timeline = TimelineEngine.build(partial_obj)
        partial_obj['timeline'] = timeline

        # ── Phase 18: AI Context Engine ───────────────────────────────────
        ai_context = AIContextEngine.generate(partial_obj)

        # Master Horoscope Structure — v4.0.0
        master_obj = {
            "engine_metadata": {
                "engine_name": "Shunyaki Vedic Astrology Engine",
                "engine_version": "4.0.0",
                "calculation_version": "1.0",
                "settings_hash": settings_hash,
                "timestamp": local_dt.isoformat()
            },
            # ── Core Birth & Astronomical Data ────────────────────────────
            "birth_data": birth_data_dict,
            "astronomical_data": asdict(astro_data),
            # ── Core Planetary & House Calculations ───────────────────────
            "planets": planets_dict,
            "houses": asdict(house_data),
            "divisional_charts": div_charts,
            "special_points": {k: asdict(v) for k, v in special_points.items()},
            "arudhas": {k: asdict(v) for k, v in arudhas.items()},
            "shadbala": shadbala_dict,
            "ishta_kashta": ishta_kashta,
            "ashtakavarga": ashtakavarga,
            "dasha": {
                "vimshottari": vimshottari,
                "yogini": yogini
            },
            "panchanga": asdict(panchanga),
            "yogas": [asdict(y) for y in yogas],
            "transits": transits_clean,
            # ── Phase 1: Validation ───────────────────────────────────────
            "validation": validation_result,
            # ── Phase 2 & 3: Aspects & Conjunctions ──────────────────────
            "planetary_aspects": aspect_result["planetary_aspects"],
            "rashi_aspects": aspect_result["rashi_aspects"],
            "conjunctions": conjunction_result["conjunctions"],
            "planetary_wars": conjunction_result["planetary_wars"],
            "stelliums": conjunction_result["stelliums"],
            # ── Phase 4: Dignity ──────────────────────────────────────────
            "dignity": dignity_result,
            # ── Phase 5: House Analysis ───────────────────────────────────
            "house_analysis": house_analysis,
            # ── Phase 6: Functional Planet Classification ─────────────────
            "functional_classification": functional_class,
            # ── Phase 7: Planet Strength Ranking ─────────────────────────
            "planet_ranking": planet_ranking,
            # ── Phase 8: Yoga Data ────────────────────────────────────────
            "advanced_yogas": advanced_yogas,   # classical Vedic yogas (100+)
            "all_yogas": all_yoga_dicts,         # merged: classical + advanced (Q3: single unified list)
            # ── Phase 9: Deterministic Rule Matches ───────────────────────
            "rule_matches": rule_matches,
            # ── Phase 10: Event Indicators ────────────────────────────────
            "event_indicators": event_indicators,
            # ── Phase 11: Prediction Index ────────────────────────────────
            "prediction_index": prediction_index,
            # ── Phase 12: Planet State (multi-dimensional strength) ────────
            "planet_state": planet_state,
            # ── Phase 13: Planet Influence Network ────────────────────────
            "planet_influence_network": planet_network,
            # ── Phase 14: House Dependency Graph ──────────────────────────
            "house_graph": house_graph,
            # ── Phase 15: Evidence Registry ───────────────────────────────
            "evidence_registry": evidence_registry,
            # ── Phase 16: Domain Synthesis ────────────────────────────────
            "domain_synthesis": domain_synthesis,
            # ── Phase 17: Timeline ────────────────────────────────────────
            "timeline": timeline,
            # ── Phase 18: AI Context (replaces ai_graph) ──────────────────
            "ai_graph": ai_graph,         # backward compat
            "ai_context": ai_context,     # v4.0 enriched context
            # ── Engine Versions ───────────────────────────────────────────
            "engine_versions": ENGINE_VERSIONS,
            # ── Backward-Compatible Status ────────────────────────────────
            "status": "success"
        }

        return master_obj
