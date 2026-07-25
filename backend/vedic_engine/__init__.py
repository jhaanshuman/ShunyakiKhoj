# -*- coding: utf-8 -*-
"""
Professional Vedic Astrology Engine Package — v4.0.0
Deterministic Reasoning Platform with full evidence chains and AI context.
"""
__version__ = "4.0.0"

# Core calculation engines
from .master_horoscope import MasterHoroscopeBuilder

# v3.0 rule & prediction engines
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
from .validation_engine import ValidationEngine

# v4.0 reasoning engines
from .planet_state_engine import PlanetStateEngine
from .planet_influence_network import PlanetInfluenceNetwork
from .house_graph_engine import HouseGraphEngine
from .evidence_engine import EvidenceEngine
from .domain_synthesis_engine import DomainSynthesisEngine
from .timeline_engine import TimelineEngine
from .ai_context_engine import AIContextEngine
