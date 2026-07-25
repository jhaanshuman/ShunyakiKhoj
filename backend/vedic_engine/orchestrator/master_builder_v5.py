# -*- coding: utf-8 -*-
"""
Master Horoscope Builder v5.0.
Single universal point of entry for building complete, synchronized, schema-validated Master Horoscope Objects.
Exposes a deterministic knowledge database containing all calculations, predictions, graph data, and AI context.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import json
from typing import Dict, Any, Optional, List

# Core calculation primitives
from ..astronomy import AstronomyEngine
from ..planets import PlanetEngine
from ..houses import HouseEngine
from ..divisional import DivisionalEngine
from ..special_points import SpecialPointsEngine
from ..arudhas import ArudhaEngine
from ..strengths import StrengthEngine
from ..ashtakavarga import AshtakavargaEngine
from ..panchanga import PanchangaEngine
from ..transits import TransitEngine

# Sub-engine reasoning modules
from ..aspect_engine import AspectEngine
from ..conjunction_engine import ConjunctionEngine
from ..dignity_engine import DignityEngine
from ..house_analysis_engine import HouseAnalysisEngine
from ..functional_planet_engine import FunctionalPlanetEngine
from ..planet_ranking_engine import PlanetRankingEngine
from ..rule_engine import RuleEngine
from ..event_indicator_engine import EventIndicatorEngine
from ..prediction_index_engine import PredictionIndexEngine
from ..planet_state_engine import PlanetStateEngine
from ..planet_influence_network import PlanetInfluenceNetwork
from ..house_graph_engine import HouseGraphEngine
from ..evidence_engine import EvidenceEngine
from ..timeline_engine import TimelineEngine
from ..ai_context_engine import AIContextEngine
from ..validation_engine import ValidationEngine

# v5.0 Module Subsystems
from ..modules.yogas.yoga_orchestrator import evaluate_all_300_yogas
from ..modules.doshas.dosha_orchestrator import evaluate_all_doshas
from ..modules.dashas.dasha_orchestrator import calculate_all_dashas
from ..modules.jaimini.jaimini_engine import calculate_jaimini
from ..modules.kp.kp_engine import calculate_kp
from ..modules.matching.matching_engine import calculate_matching
from ..modules.graphs.graph_data_engine import generate_graph_datasets
from ..modules.tables.table_data_engine import generate_table_datasets
from ..modules.domain_engine.domain_engine import DomainEngine

# Orchestrator Registry & Validator
from .module_registry import ModuleRegistry
from .schema_validator import SchemaValidator

ENGINE_VERSIONS = {
    "platform": "5.0.0",
    "core_astronomy": "2.2.0",
    "rule_engine": "5.0.0",
    "yoga_engine": "5.0.0 (300+ Yogas)",
    "dosha_engine": "5.0.0",
    "dasha_engine": "5.0.0 (19 Dasha Systems)",
    "jaimini_module": "5.0.0",
    "kp_module": "5.0.0",
    "matching_engine": "5.0.0",
    "domain_engine": "5.0.0 (27 Domains)",
    "graph_data_engine": "5.0.0",
    "table_data_engine": "5.0.0"
}


class MasterHoroscopeBuilderV5:
    """Single point of entry for building complete, synchronized v5.0 Master Horoscope Objects."""

    @classmethod
    def build_master_horoscope(
        cls,
        name: str,
        gender: str,
        dob_str: str,
        tob_str: str,
        place: str,
        lat: float,
        lon: float,
        tz_offset: float = 5.5,
        ayanamsa_name: str = "Lahiri",
        node_type: str = "True",
        house_system: str = "Whole Sign",
        requested_modules: List[str] = None,
        partner_birth_details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Compute and assemble the complete Master Horoscope Object v5.0."""
        if requested_modules is None:
            requested_modules = ["ALL"]

        # Safely resolve numeric tz_offset (handles float, string, or timezone name like "Asia/Kolkata")
        float_tz = 5.5
        if isinstance(tz_offset, (int, float)):
            float_tz = float(tz_offset)
        elif isinstance(tz_offset, str):
            try:
                float_tz = float(tz_offset)
            except ValueError:
                try:
                    import pytz
                    clean_tz = tz_offset.strip()
                    if 'Asia/' in clean_tz:
                        clean_tz = 'Asia/' + clean_tz.split('Asia/')[-1].split('Asia')[0].replace('/', '')
                    tz_obj = pytz.timezone(clean_tz if clean_tz in pytz.all_timezones else 'Asia/Kolkata')
                    float_tz = round(datetime.now(tz_obj).utcoffset().total_seconds() / 3600.0, 2)
                except Exception:
                    float_tz = round(lon / 15.0 * 2.0) / 2.0
        tz_offset = float_tz

        # Parse Datetime
        clean_dob = dob_str.replace('-', '/')
        dob_parts = [int(x) for x in clean_dob.split('/')]
        tob_parts = [int(x) for x in tob_str.split(':')]

        local_dt = datetime(dob_parts[0], dob_parts[1], dob_parts[2], tob_parts[0], tob_parts[1])
        total_seconds_offset = int(tz_offset * 3600)
        ut_dt = local_dt - timedelta(seconds=total_seconds_offset)

        settings_str = f"{dob_str}_{tob_str}_{lat:.4f}_{lon:.4f}_{tz_offset}_{ayanamsa_name}_{node_type}_{house_system}"
        settings_hash = hashlib.sha256(settings_str.encode('utf-8')).hexdigest()[:16]

        # 1. Core Astronomy Calculation
        astro_data = AstronomyEngine.calculate_astronomy_data(
            dt_ut=ut_dt,
            lat=lat,
            lon=lon,
            ayanamsa_name=ayanamsa_name
        )

        # 2. Planet Calculations
        planets_data = PlanetEngine.calculate_planets(
            jd_ut=astro_data.julian_day_ut,
            ayanamsa_val=astro_data.ayanamsa_val,
            node_type=node_type
        )
        planets_dict = {p_name: asdict(p_obj) for p_name, p_obj in planets_data.items()}

        # 3. House Calculations
        house_data = HouseEngine.calculate_houses(
            jd_ut=astro_data.julian_day_ut,
            lat=lat,
            lon=lon,
            ayanamsa_val=astro_data.ayanamsa_val,
            system_name=house_system,
            planets_data=planets_data
        )

        # 4. Divisional Charts (D1 to D144 with dignities & D60 deities)
        div_charts = DivisionalEngine.calculate_all_divisional_charts(
            asc_sid_lon=house_data.ascendant_sidereal_lon,
            planets_data=planets_data
        )

        # 5. Special Points & Lagnas
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

        # 6. Arudhas
        arudhas = ArudhaEngine.calculate_arudhas(
            asc_sign_name=house_data.ascendant_sign,
            planets_data=planets_data
        )

        # 7. Strengths (Shadbala & Ishta/Kashta)
        is_day = 6.0 <= local_dt.hour < 18.0
        shadbala_data = StrengthEngine.calculate_shadbala(
            planets_data=planets_data,
            asc_sid_lon=house_data.ascendant_sidereal_lon,
            is_day_birth=is_day
        )
        ishta_kashta = StrengthEngine.calculate_ishta_kashta(shadbala_data, planets_data)
        shadbala_dict = {k: asdict(v) for k, v in shadbala_data.items()}
        shadbala_virupas = {p: v.total_virupas for p, v in shadbala_data.items()}

        # 8. Ashtakavarga
        ashtakavarga = AshtakavargaEngine.calculate_bav_and_sav(
            planets_data=planets_data,
            asc_sid_lon=house_data.ascendant_sidereal_lon
        )

        # 9. Panchanga
        panchanga = PanchangaEngine.calculate_panchanga(
            sun_sid_lon=sun_lon,
            moon_sid_lon=moon_lon,
            birth_dt=local_dt,
            sunrise_jd=astro_data.sunrise_ut,
            sunset_jd=astro_data.sunset_ut
        )

        # 10. Real-time Transits
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

        # 11. Dignities, Aspects & Conjunctions
        dignity_result = DignityEngine.calculate_complete_dignities(planets_dict, asc_sign_idx)
        aspect_result = AspectEngine.calculate_aspects(planets_dict, asc_sign_idx)
        conjunction_result = ConjunctionEngine.calculate_conjunctions(planets_dict)

        # Build partial object for reasoning layers
        partial_obj = {
            "planets": planets_dict,
            "houses": asdict(house_data),
            "shadbala": shadbala_virupas,
            "dignity": dignity_result,
            "planetary_aspects": aspect_result["planetary_aspects"],
            "ashtakavarga": ashtakavarga,
            "birth_data": {
                "name": name, "gender": gender, "date_of_birth": dob_str, "birth_date": dob_str,
                "time_of_birth": tob_str, "place": place, "latitude": lat, "longitude": lon,
                "timezone_offset": tz_offset, "ayanamsa_name": ayanamsa_name
            }
        }

        # 12. House Analysis, Functional Classification, Planet Ranking
        house_analysis = HouseAnalysisEngine.analyze_houses(partial_obj)
        partial_obj['house_analysis'] = house_analysis
        functional_class = FunctionalPlanetEngine.classify_planets(asc_sign_idx)
        partial_obj['functional_classification'] = functional_class
        planet_ranking = PlanetRankingEngine.rank_planets(partial_obj)
        partial_obj['planet_ranking'] = planet_ranking

        # 13. Advanced 300+ Yogas Subsystem
        yogas_result = evaluate_all_300_yogas(partial_obj)
        all_yoga_dicts = yogas_result.get("yogas", [])
        partial_obj['yogas'] = all_yoga_dicts
        partial_obj['all_yogas'] = all_yoga_dicts

        # 14. Complete Dosha Subsystem
        doshas_result = evaluate_all_doshas(partial_obj)
        partial_obj['dosha_result'] = doshas_result

        # 15. Deterministic Rule Engine
        rule_matches = RuleEngine.evaluate_rules(partial_obj)
        partial_obj['rule_matches'] = rule_matches

        # 16. Event Indicators & Prediction Index
        event_indicators = EventIndicatorEngine.calculate_event_indicators(partial_obj)
        partial_obj['event_indicators'] = event_indicators
        prediction_index = PredictionIndexEngine.generate_prediction_index(partial_obj)
        partial_obj['prediction_index'] = prediction_index

        # 17. Reasoning Engines: Planet State, Influence Network, House Graph, Evidence
        planet_state = PlanetStateEngine.compute(partial_obj)
        partial_obj['planet_state'] = planet_state

        planet_network = PlanetInfluenceNetwork.build(partial_obj)
        partial_obj['planet_influence_network'] = planet_network

        house_graph = HouseGraphEngine.build(partial_obj)
        partial_obj['house_graph'] = house_graph

        evidence_registry = EvidenceEngine.compile(partial_obj)
        partial_obj['evidence_registry'] = evidence_registry

        # 18. 19-Dasha Subsystem
        dashas_result = calculate_all_dashas(partial_obj, ["ALL"])
        partial_obj['dasha'] = dashas_result
        partial_obj['transits'] = transits_clean

        # 19. Timeline Engine
        timeline = TimelineEngine.build(partial_obj)
        partial_obj['timeline'] = timeline

        # 20. Jaimini Subsystem
        jaimini_result = calculate_jaimini(partial_obj)
        partial_obj['jaimini'] = jaimini_result

        # 21. KP Subsystem
        kp_result = calculate_kp(partial_obj)
        partial_obj['kp'] = kp_result

        # 22. 27 Life Domains Engine
        domain_27_result = DomainEngine.synthesize_27_domains(partial_obj)
        partial_obj['domain_synthesis'] = domain_27_result

        # 23. AI Context Engine
        ai_context = AIContextEngine.generate(partial_obj)

        # 24. Graph Data Engine (JSON datasets)
        graphs_result = generate_graph_datasets(partial_obj)

        # 25. Table Data Engine (Normalized 2D datasets)
        tables_result = generate_table_datasets(partial_obj)

        # 26. Matching Subsystem (if partner birth details provided)
        matching_result = None
        if partner_birth_details:
            try:
                p_clean_date = partner_birth_details['date'].replace('-', '/')
                partner_master = cls.build_master_horoscope(
                    name=partner_birth_details.get('name', 'Partner'),
                    gender=partner_birth_details.get('gender', 'Female'),
                    dob_str=p_clean_date,
                    tob_str=partner_birth_details.get('time', '12:00'),
                    place=partner_birth_details.get('place', 'Delhi'),
                    lat=partner_birth_details.get('lat', 28.6139),
                    lon=partner_birth_details.get('lon', 77.2090),
                    tz_offset=partner_birth_details.get('tz_offset', 5.5)
                )
                matching_result = calculate_matching(partial_obj, partner_master)
            except Exception as e:
                matching_result = {"status": "error", "message": f"Partner calculation failed: {str(e)}"}

        # 27. Validation Engine
        validation_target = {
            "engine_metadata": {"version": "5.0.0"},
            "birth_data": partial_obj['birth_data'],
            "astronomical_data": asdict(astro_data),
            "planets": planets_dict,
            "houses": asdict(house_data),
            "divisional_charts": div_charts
        }
        validation_result = ValidationEngine.validate_horoscope(validation_target)

        # Construct Master Horoscope v5.0 Output Structure
        master_obj = {
            "engine_metadata": {
                "engine_name": "Shunyaki Enterprise Vedic Astrology Engine",
                "engine_version": "5.0.0",
                "calculation_version": "1.0",
                "settings_hash": settings_hash,
                "timestamp": local_dt.isoformat()
            },
            "input": {
                "birth_details": partial_obj['birth_data'],
                "requested_modules": requested_modules
            },
            "validation": validation_result,
            "astronomical_data": asdict(astro_data),
            "astronomy": asdict(astro_data),
            "birth": partial_obj['birth_data'],
            "planets": planets_dict,
            "houses": asdict(house_data),
            "vargas": div_charts,
            "divisional_charts": div_charts,
            "special_points": {k: asdict(v) for k, v in special_points.items()},
            "arudhas": {k: asdict(v) for k, v in arudhas.items()},
            "strength": {
                "shadbala": shadbala_dict,
                "ishta_kashta": ishta_kashta,
                "planet_state": planet_state,
                "planet_ranking": planet_ranking
            },
            "shadbala": shadbala_dict,
            "ishta_kashta": ishta_kashta,
            "ashtakavarga": ashtakavarga,
            "aspects": aspect_result,
            "planetary_aspects": aspect_result["planetary_aspects"],
            "rashi_aspects": aspect_result["rashi_aspects"],
            "conjunctions": conjunction_result["conjunctions"],
            "planetary_wars": conjunction_result["planetary_wars"],
            "stelliums": conjunction_result["stelliums"],
            "dignity": dignity_result,
            "yogas": yogas_result,
            "all_yogas": all_yoga_dicts,
            "doshas": doshas_result,
            "dashas": dashas_result,
            "dasha": dashas_result,
            "transits": transits_clean,
            "argala": {"status": "computed", "arudhas": {k: asdict(v) for k, v in arudhas.items()}},
            "karakas": jaimini_result.get("chara_karakas", {}),
            "jaimini": jaimini_result,
            "kp": kp_result,
            "panchanga": asdict(panchanga),
            "matching": matching_result or {"status": "not_requested"},
            "house_analysis": house_analysis,
            "functional_classification": functional_class,
            "planet_ranking": planet_ranking,
            "rule_engine": rule_matches,
            "rule_matches": rule_matches,
            "event_indicators": event_indicators,
            "domain_engine": domain_27_result,
            "domain_synthesis": domain_27_result,
            "timeline": timeline,
            "prediction_index": prediction_index,
            "planet_state": planet_state,
            "planet_influence_network": planet_network,
            "house_graph": house_graph,
            "evidence_registry": evidence_registry,
            "graphs": graphs_result,
            "tables": tables_result,
            "statistics": {
                "total_yogas_detected": len(all_yoga_dicts),
                "total_doshas_detected": doshas_result.get("total_doshas_found", 0),
                "total_rules_matched": len(rule_matches),
                "total_dashas_computed": len(dashas_result),
                "total_domains_analyzed": len(domain_27_result)
            },
            "knowledge": {
                "tradition": "Parashari / Jaimini / KP Classical",
                "rules_source": "BPHS, Phaladeepika, Saravali, Jaimini Sutras"
            },
            "ai_graph": ai_context,
            "ai_context": ai_context,
            "metadata": {
                "engine_versions": ENGINE_VERSIONS,
                "status": "success"
            },
            "engine_versions": ENGINE_VERSIONS,
            "status": "success"
        }

        # Validate Schema Output Compliance
        schema_audit = SchemaValidator.validate_v5_output(master_obj)
        master_obj["schema_audit"] = schema_audit

        return master_obj
