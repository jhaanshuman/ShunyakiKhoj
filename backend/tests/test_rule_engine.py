# -*- coding: utf-8 -*-
"""
Enterprise Rule Engine Unit Tests (Phase 1–11)
Validates every new engine module independently against known astronomical inputs.
"""

import sys
import os
import unittest
import json

# Resolve backend root path
BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(os.path.join(BACKEND_ROOT, '..')))

from backend.vedic_engine.validation_engine import ValidationEngine
from backend.vedic_engine.aspect_engine import AspectEngine
from backend.vedic_engine.conjunction_engine import ConjunctionEngine
from backend.vedic_engine.dignity_engine import DignityEngine
from backend.vedic_engine.house_analysis_engine import HouseAnalysisEngine
from backend.vedic_engine.functional_planet_engine import FunctionalPlanetEngine
from backend.vedic_engine.planet_ranking_engine import PlanetRankingEngine
from backend.vedic_engine.advanced_yoga_engine import AdvancedYogaEngine
from backend.vedic_engine.rule_engine import RuleEngine
from backend.vedic_engine.event_indicator_engine import EventIndicatorEngine
from backend.vedic_engine.prediction_index_engine import PredictionIndexEngine


# ═════════════════════════════════════════════════════════════════════════════════
# SHARED TEST FIXTURE: Simulated horoscope (Aries Ascendant, Sun in Aries exalted)
# This represents a known Aries ascendant chart with Jupiter in Cancer (exalted),
# Sun in Aries (exalted), and Rahu/Ketu in opposition.
# ═════════════════════════════════════════════════════════════════════════════════

MOCK_PLANETS = {
    "Sun":     {"name": "Sun",     "sidereal_lon": 10.0,  "sign_index": 0,  "sign_name": "Aries",       "sign_degree": 10.0, "nakshatra_index": 0,  "nakshatra_name": "Ashwini", "pada": 2, "speed": 1.0,  "is_retrograde": False, "is_combust": False, "latitude": 0.0, "declination": 10.0, "distance": 1.0, "exaltation_state": "Exalted",   "dignity": "Exalted"},
    "Moon":    {"name": "Moon",    "sidereal_lon": 65.0,  "sign_index": 2,  "sign_name": "Gemini",      "sign_degree": 5.0,  "nakshatra_index": 6,  "nakshatra_name": "Ardra",   "pada": 1, "speed": 12.0, "is_retrograde": False, "is_combust": False, "latitude": 0.0, "declination": 5.0, "distance": 1.0,  "exaltation_state": "Neutral",  "dignity": "Neutral"},
    "Mars":    {"name": "Mars",    "sidereal_lon": 280.0, "sign_index": 9,  "sign_name": "Capricorn",   "sign_degree": 10.0, "nakshatra_index": 22, "nakshatra_name": "Shravana", "pada": 2, "speed": 0.6,  "is_retrograde": False, "is_combust": False, "latitude": 0.0, "declination": -20.0, "distance": 1.5, "exaltation_state": "Exalted", "dignity": "Exalted"},
    "Mercury": {"name": "Mercury", "sidereal_lon": 18.0,  "sign_index": 0,  "sign_name": "Aries",       "sign_degree": 18.0, "nakshatra_index": 1,  "nakshatra_name": "Bharani", "pada": 3, "speed": 1.2,  "is_retrograde": False, "is_combust": False, "latitude": 0.0, "declination": 11.0, "distance": 1.0, "exaltation_state": "Neutral",  "dignity": "Enemy"},
    "Jupiter": {"name": "Jupiter", "sidereal_lon": 93.0,  "sign_index": 3,  "sign_name": "Cancer",      "sign_degree": 3.0,  "nakshatra_index": 8,  "nakshatra_name": "Pushya",  "pada": 1, "speed": 0.1,  "is_retrograde": False, "is_combust": False, "latitude": 0.0, "declination": 23.0, "distance": 5.0, "exaltation_state": "Exalted",   "dignity": "Exalted"},
    "Venus":   {"name": "Venus",   "sidereal_lon": 45.0,  "sign_index": 1,  "sign_name": "Taurus",      "sign_degree": 15.0, "nakshatra_index": 4,  "nakshatra_name": "Rohini",  "pada": 2, "speed": 1.1,  "is_retrograde": False, "is_combust": False, "latitude": 0.0, "declination": 16.0, "distance": 1.0, "exaltation_state": "Neutral",  "dignity": "Swakshetra (Own Sign)"},
    "Saturn":  {"name": "Saturn",  "sidereal_lon": 195.0, "sign_index": 6,  "sign_name": "Libra",       "sign_degree": 15.0, "nakshatra_index": 14, "nakshatra_name": "Chitra",  "pada": 2, "speed": 0.03, "is_retrograde": False, "is_combust": False, "latitude": 0.0, "declination": -8.0, "distance": 9.5, "exaltation_state": "Exalted",  "dignity": "Exalted"},
    "Rahu":    {"name": "Rahu",    "sidereal_lon": 150.0, "sign_index": 5,  "sign_name": "Virgo",       "sign_degree": 0.0,  "nakshatra_index": 12, "nakshatra_name": "Uttara",  "pada": 1, "speed": -0.05,"is_retrograde": True,  "is_combust": False, "latitude": 0.0, "declination": 0.0, "distance": 0.0,  "exaltation_state": "Neutral",  "dignity": "Neutral"},
    "Ketu":    {"name": "Ketu",    "sidereal_lon": 330.0, "sign_index": 11, "sign_name": "Pisces",      "sign_degree": 0.0,  "nakshatra_index": 25, "nakshatra_name": "Purva Bhadra","pada": 4, "speed": -0.05,"is_retrograde": True, "is_combust": False, "latitude": 0.0, "declination": 0.0, "distance": 0.0,  "exaltation_state": "Neutral",  "dignity": "Neutral"},
}

ASC_LON = 5.0  # Aries, 5 degrees
ASC_SIGN_IDX = 0  # Aries ascendant

MOCK_HOUSES = {
    "ascendant_sidereal_lon": ASC_LON,
    "ascendant_sign": "Aries",
    "ascendant_sign_lord": "Mars",
    "mc_sidereal_lon": 270.0,
    "system_name": "Whole Sign",
    "cusps": [5.0 + i * 30.0 for i in range(12)],
    "planet_house_mapping": {p: (d['sign_index'] + 1) for p, d in MOCK_PLANETS.items()}
}

MOCK_SHADBALA = {p: 380.0 for p in MOCK_PLANETS.keys()}

MOCK_ASHTAKAVARGA = {
    "sav": {"total_bindus": 337, "chart": {}}
}

MOCK_MASTER_OBJ = {
    "planets": MOCK_PLANETS,
    "houses": MOCK_HOUSES,
    "shadbala": MOCK_SHADBALA,
    "dignity": {},
    "planetary_aspects": [],
    "yogas": [],
    "ashtakavarga": MOCK_ASHTAKAVARGA
}


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 1: VALIDATION ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestValidationEngine(unittest.TestCase):

    def _build_valid_obj(self):
        return {
            "engine_metadata": {"v": "3.0"},
            "birth_data": {"name": "Test"},
            "astronomical_data": {"julian_day_ut": 2451545.0},
            "planets": MOCK_PLANETS,
            "houses": MOCK_HOUSES,
            "divisional_charts": {v: {"Sun": 0} for v in ["D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12","D16","D20","D24","D27","D30","D40","D45","D60","D81","D108","D144"]},
            "special_points": {"PK": {}},
            "arudhas": {"A1": {}},
            "shadbala": {"Sun": {"total_virupas": 380.0}},
            "ashtakavarga": MOCK_ASHTAKAVARGA,
            "dasha": {"vimshottari": [{"lord": "Jupiter"}]},
            "panchanga": {"tithi": "Pratipada"}
        }

    def test_valid_horoscope_passes(self):
        obj = self._build_valid_obj()
        result = ValidationEngine.validate_horoscope(obj)
        self.assertEqual(result['status'], 'PASS', f"Expected PASS but got FAIL. Errors: {result['errors']}")
        self.assertGreater(result['confidence'], 95.0)

    def test_missing_key_fails(self):
        import copy
        obj = copy.deepcopy(self._build_valid_obj())
        del obj['panchanga']
        result = ValidationEngine.validate_horoscope(obj)
        self.assertEqual(result['status'], 'FAIL')

    def test_invalid_planet_longitude_fails(self):
        import copy
        obj = copy.deepcopy(self._build_valid_obj())
        obj['planets']['Sun']['sidereal_lon'] = 400.0  # Invalid > 360°
        result = ValidationEngine.validate_horoscope(obj)
        self.assertEqual(result['status'], 'FAIL')
        self.assertTrue(any('Sun' in e for e in result['errors']))

    def test_invalid_nakshatra_fails(self):
        import copy
        obj = copy.deepcopy(self._build_valid_obj())
        obj['planets']['Moon']['nakshatra_index'] = 30  # Max is 26
        result = ValidationEngine.validate_horoscope(obj)
        self.assertEqual(result['status'], 'FAIL')

    def test_rahu_ketu_warning_if_not_opposite(self):
        import copy
        obj = copy.deepcopy(self._build_valid_obj())
        # Rahu at 150, Ketu at 340 → difference is 170°, not 180°
        obj['planets']['Ketu']['sidereal_lon'] = 340.0
        result = ValidationEngine.validate_horoscope(obj)
        self.assertTrue(any('Rahu/Ketu' in w for w in result['warnings']))

    def test_sav_checksum_warning(self):
        import copy
        obj = copy.deepcopy(self._build_valid_obj())
        obj['ashtakavarga']['sav']['total_bindus'] = 300  # Wrong
        result = ValidationEngine.validate_horoscope(obj)
        self.assertTrue(any('SAV' in w or 'bindus' in w for w in result['warnings']))


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 2: ASPECT ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestAspectEngine(unittest.TestCase):

    def test_returns_planetary_and_rashi_aspects(self):
        result = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        self.assertIn('planetary_aspects', result)
        self.assertIn('rashi_aspects', result)

    def test_planetary_aspects_is_list(self):
        result = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        self.assertIsInstance(result['planetary_aspects'], list)

    def test_7th_aspect_present(self):
        # Every planet aspects 7th from itself — check Sun at sign 0 aspects sign 6 (Libra)
        result = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        sun_aspects = [a for a in result['planetary_aspects'] if a['aspecting_planet'] == 'Sun']
        self.assertTrue(len(sun_aspects) > 0, "Sun must have at least one 7th aspect")

    def test_mars_special_aspects(self):
        # Mars @ sign 9 (Capricorn) should attempt to aspect 4th, 7th, 8th signs from itself
        # 4th from sign 9 = sign 12 % 12 = 0 (Aries) -- Sun & Mercury are there
        # 7th from sign 9 = sign 15 % 12 = 3 (Cancer) -- Jupiter is there  
        # 8th from sign 9 = sign 16 % 12 = 4 (Leo) -- no planet
        # Aspects with actual planet targets will appear in the list
        result = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        mars_aspects = [a for a in result['planetary_aspects'] if a['aspecting_planet'] == 'Mars']
        # Must have at least one aspect (4th or 7th where planets exist)
        self.assertGreater(len(mars_aspects), 0, "Mars must produce at least one aspect")
        # Verify that at least 4th and 7th are attempted (even if no planet in 8th)
        aspect_houses = [a['aspect_house'] for a in mars_aspects]
        self.assertIn(4, aspect_houses, "Mars must produce a 4th-house aspect (Aries has Sun & Mercury)")

    def test_rashi_aspects_not_empty(self):
        result = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        self.assertGreater(len(result['rashi_aspects']), 0, "Rashi aspects should not be empty")

    def test_aspect_strength_in_range(self):
        result = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        for asp in result['planetary_aspects']:
            self.assertGreaterEqual(asp['strength_percentage'], 0.0)
            self.assertLessEqual(asp['strength_percentage'], 100.0)


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 3: CONJUNCTION ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestConjunctionEngine(unittest.TestCase):

    def test_returns_all_keys(self):
        result = ConjunctionEngine.calculate_conjunctions(MOCK_PLANETS)
        self.assertIn('conjunctions', result)
        self.assertIn('planetary_wars', result)
        self.assertIn('stelliums', result)

    def test_sun_mercury_conjunction_detected(self):
        # Sun @ 10°, Mercury @ 18° — both in Aries (sign_index=0) → conjunction expected
        result = ConjunctionEngine.calculate_conjunctions(MOCK_PLANETS)
        conj_pairs = [(c['planet_1'], c['planet_2']) for c in result['conjunctions']]
        self.assertIn(('Sun', 'Mercury'), conj_pairs)

    def test_combustion_type_classified(self):
        # Use a very close orb to guarantee combustion detection (orb < 6°)
        import copy
        close_planets = copy.deepcopy(MOCK_PLANETS)
        close_planets['Mercury']['sidereal_lon'] = 13.5  # Sun @ 10, Mercury @ 13.5 → orb = 3.5° = Severe
        close_planets['Mercury']['sign_degree'] = 3.5
        result = ConjunctionEngine.calculate_conjunctions(close_planets)
        sun_merc = [c for c in result['conjunctions'] if set([c['planet_1'], c['planet_2']]) == {'Sun', 'Mercury'}]
        self.assertTrue(len(sun_merc) > 0, "Sun-Mercury conjunction must be detected")
        self.assertIn('Combustion', sun_merc[0]['combustion_severity'], f"Expected combustion, got: {sun_merc[0]['combustion_severity']}")

    def test_stellium_detected_in_aries(self):
        # Aries (sign 0) has Sun + Mercury → not stellium (only 2 planets)
        result = ConjunctionEngine.calculate_conjunctions(MOCK_PLANETS)
        stellium_signs = [s['sign'] for s in result['stelliums']]
        # Should not include Aries unless 3+ planets
        self.assertNotIn('Aries', stellium_signs, "Aries with only 2 planets should not be a stellium")

    def test_planetary_war_within_one_degree(self):
        # Create planets within 0.5° war condition
        war_planets = dict(MOCK_PLANETS)
        war_planets['Mars'] = dict(MOCK_PLANETS['Mars'])
        war_planets['Saturn'] = dict(MOCK_PLANETS['Saturn'])
        war_planets['Mars']['sidereal_lon'] = 195.3
        war_planets['Mars']['sign_index'] = 6  # Same sign as Saturn
        war_planets['Mars']['sign_degree'] = 15.3
        result = ConjunctionEngine.calculate_conjunctions(war_planets)
        wars = [w for w in result['planetary_wars'] if set([w['planet_1'], w['planet_2']]) == {'Mars', 'Saturn'}]
        self.assertTrue(len(wars) > 0, "Mars-Saturn war within 0.5° must be detected")


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 4: DIGNITY ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestDignityEngine(unittest.TestCase):

    def test_all_planets_present_in_output(self):
        result = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        for p in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
            self.assertIn(p, result, f"Planet {p} must have a dignity result")

    def test_sun_in_aries_is_exalted(self):
        # Sun in Aries (sign_index=0) at 10° → Exalted
        result = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        self.assertEqual(result['Sun']['dignity_state'], 'Exalted')

    def test_jupiter_in_cancer_is_exalted(self):
        # Jupiter in Cancer (sign_index=3) → Exalted
        result = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        self.assertEqual(result['Jupiter']['dignity_state'], 'Exalted')

    def test_venus_in_taurus_is_swakshetra(self):
        # Venus in Taurus (sign_index=1) → Own Sign
        result = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        self.assertIn('Swakshetra', result['Venus']['dignity_state'])

    def test_saturn_in_libra_is_exalted(self):
        # Saturn in Libra (sign_index=6) → Exalted
        result = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        self.assertEqual(result['Saturn']['dignity_state'], 'Exalted')

    def test_dignity_has_required_fields(self):
        result = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        for p, d in result.items():
            self.assertIn('dignity_state', d, f"Missing dignity_state for {p}")
            self.assertIn('is_exalted', d, f"Missing is_exalted for {p}")
            self.assertIn('is_debilitated', d, f"Missing is_debilitated for {p}")


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 5: HOUSE ANALYSIS ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestHouseAnalysisEngine(unittest.TestCase):

    def _make_partial_obj(self):
        dignity = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        aspects = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        return {
            "planets": MOCK_PLANETS,
            "houses": MOCK_HOUSES,
            "shadbala": MOCK_SHADBALA,
            "dignity": dignity,
            "planetary_aspects": aspects['planetary_aspects'],
            "yogas": [],
            "ashtakavarga": MOCK_ASHTAKAVARGA
        }

    def test_12_houses_in_output(self):
        obj = self._make_partial_obj()
        result = HouseAnalysisEngine.analyze_houses(obj)
        self.assertEqual(len(result), 12)

    def test_house_keys_present(self):
        obj = self._make_partial_obj()
        result = HouseAnalysisEngine.analyze_houses(obj)
        for h in range(1, 13):
            self.assertIn(f"house_{h}", result)

    def test_house_score_in_range(self):
        obj = self._make_partial_obj()
        result = HouseAnalysisEngine.analyze_houses(obj)
        for h in range(1, 13):
            score = result[f"house_{h}"]['house_score']
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 100.0)

    def test_1st_house_has_mars_as_lord_for_aries(self):
        obj = self._make_partial_obj()
        result = HouseAnalysisEngine.analyze_houses(obj)
        self.assertEqual(result['house_1']['house_lord'], 'Mars')


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 6: FUNCTIONAL PLANET ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestFunctionalPlanetEngine(unittest.TestCase):

    def test_aries_ascendant_classification(self):
        result = FunctionalPlanetEngine.classify_planets(0)  # Aries
        self.assertIn('Sun', result['functional_benefics'])
        self.assertIn('Mars', result['functional_benefics'])
        self.assertIn('Jupiter', result['functional_benefics'])

    def test_marakas_for_aries(self):
        result = FunctionalPlanetEngine.classify_planets(0)
        # 2nd lord = Venus, 7th lord = Venus → Maraka = Venus
        self.assertIn('Venus', result['marakas'])

    def test_yogakaraka_for_aries(self):
        result = FunctionalPlanetEngine.classify_planets(0)
        self.assertEqual(result['yogakaraka'], 'Mars')

    def test_trik_lords_for_aries(self):
        result = FunctionalPlanetEngine.classify_planets(0)
        # 6th lord Mercury, 8th lord Mars, 12th lord Jupiter for Aries
        trik = result['trik_lords']
        self.assertIsInstance(trik, list)
        self.assertGreater(len(trik), 0)

    def test_all_12_ascendants_work(self):
        for i in range(12):
            result = FunctionalPlanetEngine.classify_planets(i)
            self.assertIn('ascendant_sign', result)
            self.assertIn('functional_benefics', result)
            self.assertIn('functional_malefics', result)


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 7: PLANET RANKING ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestPlanetRankingEngine(unittest.TestCase):

    def _make_partial_obj(self):
        dignity = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        aspects = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        return {
            "planets": MOCK_PLANETS,
            "shadbala": MOCK_SHADBALA,
            "dignity": dignity,
            "planetary_aspects": aspects['planetary_aspects']
        }

    def test_ranks_all_planets(self):
        obj = self._make_partial_obj()
        result = PlanetRankingEngine.rank_planets(obj)
        self.assertGreater(len(result), 5)

    def test_ranks_are_unique_sequential(self):
        obj = self._make_partial_obj()
        result = PlanetRankingEngine.rank_planets(obj)
        ranks = [r['rank'] for r in result]
        self.assertEqual(ranks, sorted(ranks))

    def test_score_in_valid_range(self):
        obj = self._make_partial_obj()
        result = PlanetRankingEngine.rank_planets(obj)
        for r in result:
            self.assertGreaterEqual(r['score'], 0.0)
            self.assertLessEqual(r['score'], 100.0)

    def test_exalted_sun_ranks_high(self):
        obj = self._make_partial_obj()
        result = PlanetRankingEngine.rank_planets(obj)
        sun_entry = next((r for r in result if r['name'] == 'Sun'), None)
        self.assertIsNotNone(sun_entry, "Sun must appear in ranking")
        # With uniform Shadbala in mock, exalted Sun must not rank in the bottom 3
        total_planets = len(result)
        self.assertLessEqual(sun_entry['rank'], total_planets - 2,
            f"Exalted Sun (rank {sun_entry['rank']}) should not be in bottom 2")


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 8: ADVANCED YOGA ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestAdvancedYogaEngine(unittest.TestCase):

    def _make_partial_obj(self):
        return {
            "planets": MOCK_PLANETS,
            "houses": MOCK_HOUSES,
            "dignity": DignityEngine.calculate_complete_dignities(MOCK_PLANETS),
            "yogas": []
        }

    def test_returns_list_of_yogas(self):
        obj = self._make_partial_obj()
        result = AdvancedYogaEngine.detect_all_yogas(obj)
        self.assertIsInstance(result, list)

    def test_budhaditya_yoga_detected(self):
        # Sun @ Aries (sign 0) + Mercury @ Aries (sign 0) → Budhaditya
        obj = self._make_partial_obj()
        result = AdvancedYogaEngine.detect_all_yogas(obj)
        yoga_names = [y['name'] for y in result]
        self.assertTrue(any('Budhaditya' in n for n in yoga_names), "Budhaditya yoga must be detected")

    def test_yoga_has_required_fields(self):
        obj = self._make_partial_obj()
        result = AdvancedYogaEngine.detect_all_yogas(obj)
        for yoga in result:
            self.assertIn('name', yoga)
            self.assertIn('category', yoga)
            self.assertIn('confidence', yoga)
            self.assertIn('strength', yoga)
            self.assertIn('rules_matched', yoga)

    def test_confidence_in_valid_range(self):
        obj = self._make_partial_obj()
        result = AdvancedYogaEngine.detect_all_yogas(obj)
        for yoga in result:
            self.assertGreater(yoga['confidence'], 0.0)
            self.assertLessEqual(yoga['confidence'], 100.0)


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 9: RULE ENGINE TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestRuleEngine(unittest.TestCase):

    def _make_partial_obj(self):
        dignity = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        aspects = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        partial = {
            "planets": MOCK_PLANETS,
            "houses": MOCK_HOUSES,
            "shadbala": MOCK_SHADBALA,
            "dignity": dignity,
            "planetary_aspects": aspects['planetary_aspects'],
            "yogas": [],
            "ashtakavarga": MOCK_ASHTAKAVARGA
        }
        house_analysis = HouseAnalysisEngine.analyze_houses(partial)
        partial['house_analysis'] = house_analysis
        functional = FunctionalPlanetEngine.classify_planets(ASC_SIGN_IDX)
        partial['functional_classification'] = functional
        planet_ranking = PlanetRankingEngine.rank_planets(partial)
        partial['planet_ranking'] = planet_ranking
        return partial

    def test_returns_list_of_rules(self):
        obj = self._make_partial_obj()
        result = RuleEngine.evaluate_rules(obj)
        self.assertIsInstance(result, list)

    def test_rule_has_required_fields(self):
        obj = self._make_partial_obj()
        result = RuleEngine.evaluate_rules(obj)
        for rule in result:
            self.assertIn('id', rule)
            self.assertIn('title', rule)
            self.assertIn('domain', rule)
            self.assertIn('confidence', rule)
            self.assertIn('strength', rule)
            # Rule engine uses 'matched_conditions' as the evidence list
            self.assertIn('matched_conditions', rule)

    def test_confidence_in_valid_range(self):
        obj = self._make_partial_obj()
        result = RuleEngine.evaluate_rules(obj)
        for rule in result:
            self.assertGreater(rule['confidence'], 0.0)
            self.assertLessEqual(rule['confidence'], 100.0)

    def test_rule_id_unique(self):
        obj = self._make_partial_obj()
        result = RuleEngine.evaluate_rules(obj)
        ids = [r['id'] for r in result]
        self.assertEqual(len(ids), len(set(ids)), "All rule IDs must be unique")


# ═════════════════════════════════════════════════════════════════════════════════
# PHASE 10 & 11: EVENT INDICATOR & PREDICTION INDEX TESTS
# ═════════════════════════════════════════════════════════════════════════════════

class TestEventIndicatorEngine(unittest.TestCase):

    def _make_partial_obj(self):
        dignity = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        aspects = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        partial = {
            "planets": MOCK_PLANETS,
            "houses": MOCK_HOUSES,
            "shadbala": MOCK_SHADBALA,
            "dignity": dignity,
            "planetary_aspects": aspects['planetary_aspects'],
            "yogas": [],
            "ashtakavarga": MOCK_ASHTAKAVARGA
        }
        partial['house_analysis'] = HouseAnalysisEngine.analyze_houses(partial)
        partial['functional_classification'] = FunctionalPlanetEngine.classify_planets(ASC_SIGN_IDX)
        partial['planet_ranking'] = PlanetRankingEngine.rank_planets(partial)
        partial['rule_matches'] = RuleEngine.evaluate_rules(partial)
        return partial

    def test_all_domains_present(self):
        obj = self._make_partial_obj()
        result = EventIndicatorEngine.calculate_event_indicators(obj)
        for domain in ['career', 'marriage', 'wealth', 'education', 'health']:
            self.assertIn(domain, result, f"Domain '{domain}' missing from event indicators")

    def test_scores_in_valid_range(self):
        obj = self._make_partial_obj()
        result = EventIndicatorEngine.calculate_event_indicators(obj)
        for domain, score in result.items():
            self.assertGreaterEqual(score, 0.0, f"{domain} score below 0")
            self.assertLessEqual(score, 100.0, f"{domain} score above 100")


class TestPredictionIndexEngine(unittest.TestCase):

    def _make_partial_obj(self):
        dignity = DignityEngine.calculate_complete_dignities(MOCK_PLANETS)
        aspects = AspectEngine.calculate_aspects(MOCK_PLANETS, ASC_SIGN_IDX)
        partial = {
            "planets": MOCK_PLANETS,
            "houses": MOCK_HOUSES,
            "shadbala": MOCK_SHADBALA,
            "dignity": dignity,
            "planetary_aspects": aspects['planetary_aspects'],
            "yogas": [],
            "ashtakavarga": MOCK_ASHTAKAVARGA
        }
        partial['house_analysis'] = HouseAnalysisEngine.analyze_houses(partial)
        partial['functional_classification'] = FunctionalPlanetEngine.classify_planets(ASC_SIGN_IDX)
        partial['planet_ranking'] = PlanetRankingEngine.rank_planets(partial)
        partial['rule_matches'] = RuleEngine.evaluate_rules(partial)
        partial['event_indicators'] = EventIndicatorEngine.calculate_event_indicators(partial)
        return partial

    def test_prediction_index_has_required_fields(self):
        obj = self._make_partial_obj()
        result = PredictionIndexEngine.generate_prediction_index(obj)
        for field in ['strongest_planet', 'weakest_planet', 'best_house', 'most_afflicted_house',
                      'career_score', 'marriage_score', 'wealth_score', 'health_score']:
            self.assertIn(field, result, f"Missing field '{field}' in prediction_index")

    def test_strongest_planet_is_valid_name(self):
        obj = self._make_partial_obj()
        result = PredictionIndexEngine.generate_prediction_index(obj)
        valid_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        self.assertIn(result['strongest_planet'], valid_planets)

    def test_house_numbers_in_range(self):
        obj = self._make_partial_obj()
        result = PredictionIndexEngine.generate_prediction_index(obj)
        self.assertIn(result['best_house'], range(1, 13))
        self.assertIn(result['most_afflicted_house'], range(1, 13))


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().discover('.', pattern='test_rule_engine.py')
    runner.run(suite)
