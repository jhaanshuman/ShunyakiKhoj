# -*- coding: utf-8 -*-
"""
Shunyaki Vedic Astrology Platform Package — v5.0.0
Universal Enterprise Vedic Astrology Engine & API
"""

__version__ = "5.0.0"

# Core Master Orchestrator v5.0
from .orchestrator.master_builder_v5 import MasterHoroscopeBuilderV5
from .master_horoscope import MasterHoroscopeBuilder

# Core calculation engines
from .astronomy import AstronomyEngine
from .planets import PlanetEngine
from .houses import HouseEngine
from .divisional import DivisionalEngine
from .special_points import SpecialPointsEngine
from .arudhas import ArudhaEngine
from .strengths import StrengthEngine
from .ashtakavarga import AshtakavargaEngine
from .panchanga import PanchangaEngine
from .transits import TransitEngine

# Sub-engine reasoning modules
from .aspect_engine import AspectEngine
from .conjunction_engine import ConjunctionEngine
from .dignity_engine import DignityEngine
from .house_analysis_engine import HouseAnalysisEngine
from .functional_planet_engine import FunctionalPlanetEngine
from .planet_ranking_engine import PlanetRankingEngine
from .rule_engine import RuleEngine
from .event_indicator_engine import EventIndicatorEngine
from .prediction_index_engine import PredictionIndexEngine
from .planet_state_engine import PlanetStateEngine
from .planet_influence_network import PlanetInfluenceNetwork
from .house_graph_engine import HouseGraphEngine
from .evidence_engine import EvidenceEngine
from .timeline_engine import TimelineEngine
from .ai_context_engine import AIContextEngine
from .validation_engine import ValidationEngine

# v5.0 Subsystems
from .modules.yogas.yoga_orchestrator import evaluate_all_300_yogas
from .modules.doshas.dosha_orchestrator import evaluate_all_doshas
from .modules.dashas.dasha_orchestrator import calculate_all_dashas
from .modules.jaimini.jaimini_engine import calculate_jaimini
from .modules.kp.kp_engine import calculate_kp
from .modules.matching.matching_engine import calculate_matching
from .modules.graphs.graph_data_engine import generate_graph_datasets
from .modules.tables.table_data_engine import generate_table_datasets
from .modules.domain_engine.domain_engine import DomainEngine
from .orchestrator.module_registry import ModuleRegistry
from .orchestrator.schema_validator import SchemaValidator
