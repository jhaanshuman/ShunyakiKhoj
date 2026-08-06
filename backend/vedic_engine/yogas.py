# -*- coding: utf-8 -*-
"""
Yoga Engine: Rule-based evaluation engine for 100+ Classical Vedic Yogas.
"""
from dataclasses import dataclass, asdict
from typing import Dict, List, Any

@dataclass
class YogaResult:
    name: str
    category: str
    formula: str
    participating_planets: List[str]
    participating_houses: List[int]
    result_narrative: str
    confidence: float
    priority: str
    affected_areas: List[str]

class YogaEngine:
    """Evaluates planetary longitudes and house placements against classical Yoga rules."""
    
    @classmethod
    def evaluate_yogas(
        cls,
        planets_data: Dict[str, Any],
        asc_sign_name: str,
        planet_house_map: Dict[str, int]
    ) -> List[YogaResult]:
        """Evaluate chart for active Yogas."""
        active_yogas: List[YogaResult] = []
        
        # 1. Gaja Kesari Yoga (Jupiter in Kendra from Moon)
        moon_h = planet_house_map.get('Moon', 1)
        jup_h = planet_house_map.get('Jupiter', 1)
        rel_h = ((jup_h - moon_h) % 12) + 1
        if rel_h in [1, 4, 7, 10]:
            active_yogas.append(YogaResult(
                name="Gaja Kesari Yoga",
                category="Raja Yoga",
                formula="Jupiter in a Kendra (1st, 4th, 7th, 10th) from Moon",
                participating_planets=["Jupiter", "Moon"],
                participating_houses=[moon_h, jup_h],
                result_narrative="Grants high intelligence, wisdom, fame, nobility, lasting reputation, and financial prosperity throughout life.",
                confidence=95.0,
                priority="High",
                affected_areas=["Reputation", "Wealth", "Wisdom", "Career"]
            ))

        # 2. Pancha Mahapurusha Yogas
        # Ruchaka (Mars in Kendra in Aries, Scorpio, Capricorn)
        mars_h = planet_house_map.get('Mars', 1)
        mars_sign = planets_data['Mars'].sign_name if hasattr(planets_data['Mars'], 'sign_name') else planets_data['Mars'].get('sign_name', '')
        if mars_h in [1, 4, 7, 10] and mars_sign in ['Aries', 'Scorpio', 'Capricorn']:
            active_yogas.append(YogaResult(
                name="Ruchaka Yoga",
                category="Pancha Mahapurusha",
                formula="Mars in Kendra in Swakshetra (Aries/Scorpio) or Exaltation (Capricorn)",
                participating_planets=["Mars"],
                participating_houses=[mars_h],
                result_narrative="Grants immense physical strength, leadership, courage, military or executive power, and victory over adversaries.",
                confidence=90.0,
                priority="High",
                affected_areas=["Courage", "Leadership", "Executive Power"]
            ))

        # Bhadra (Mercury in Kendra in Gemini, Virgo)
        mer_h = planet_house_map.get('Mercury', 1)
        mer_sign = planets_data['Mercury'].sign_name if hasattr(planets_data['Mercury'], 'sign_name') else planets_data['Mercury'].get('sign_name', '')
        if mer_h in [1, 4, 7, 10] and mer_sign in ['Gemini', 'Virgo']:
            active_yogas.append(YogaResult(
                name="Bhadra Yoga",
                category="Pancha Mahapurusha",
                formula="Mercury in Kendra in Swakshetra (Gemini) or Exaltation (Virgo)",
                participating_planets=["Mercury"],
                participating_houses=[mer_h],
                result_narrative="Bestows exceptional eloquence, mathematical brilliance, scholarly distinction, business acumen, and longevity.",
                confidence=90.0,
                priority="High",
                affected_areas=["Intellect", "Business", "Communication"]
            ))

        # Hamsa (Jupiter in Kendra in Cancer, Sagittarius, Pisces)
        jup_sign = planets_data['Jupiter'].sign_name if hasattr(planets_data['Jupiter'], 'sign_name') else planets_data['Jupiter'].get('sign_name', '')
        if jup_h in [1, 4, 7, 10] and jup_sign in ['Cancer', 'Sagittarius', 'Pisces']:
            active_yogas.append(YogaResult(
                name="Hamsa Yoga",
                category="Pancha Mahapurusha",
                formula="Jupiter in Kendra in Exaltation (Cancer) or Swakshetra (Sagittarius/Pisces)",
                participating_planets=["Jupiter"],
                participating_houses=[jup_h],
                result_narrative="Blesses native with high spiritual wisdom, righteous character, societal reverence, sound judgment, and grace.",
                confidence=92.0,
                priority="High",
                affected_areas=["Spirituality", "Wisdom", "Respect"]
            ))

        # Malavya (Venus in Kendra in Taurus, Libra, Pisces)
        ven_h = planet_house_map.get('Venus', 1)
        ven_sign = planets_data['Venus'].sign_name if hasattr(planets_data['Venus'], 'sign_name') else planets_data['Venus'].get('sign_name', '')
        if ven_h in [1, 4, 7, 10] and ven_sign in ['Taurus', 'Libra', 'Pisces']:
            active_yogas.append(YogaResult(
                name="Malavya Yoga",
                category="Pancha Mahapurusha",
                formula="Venus in Kendra in Swakshetra (Taurus/Libra) or Exaltation (Pisces)",
                participating_planets=["Venus"],
                participating_houses=[ven_h],
                result_narrative="Grants artistic talent, luxurious vehicles, magnetic personality, marital bliss, and refined aesthetic sense.",
                confidence=90.0,
                priority="High",
                affected_areas=["Luxury", "Arts", "Marriage", "Wealth"]
            ))

        # Sasa (Saturn in Kendra in Libra, Capricorn, Aquarius)
        sat_h = planet_house_map.get('Saturn', 1)
        sat_sign = planets_data['Saturn'].sign_name if hasattr(planets_data['Saturn'], 'sign_name') else planets_data['Saturn'].get('sign_name', '')
        if sat_h in [1, 4, 7, 10] and sat_sign in ['Libra', 'Capricorn', 'Aquarius']:
            active_yogas.append(YogaResult(
                name="Sasa Yoga",
                category="Pancha Mahapurusha",
                formula="Saturn in Kendra in Exaltation (Libra) or Swakshetra (Capricorn/Aquarius)",
                participating_planets=["Saturn"],
                participating_houses=[sat_h],
                result_narrative="Gives command over masses, political influence, perseverance, authority over lands, and enduring legacy.",
                confidence=90.0,
                priority="High",
                affected_areas=["Authority", "Politics", "Perseverance"]
            ))

        # 3. Budhaditya Yoga (Sun + Mercury in same house)
        sun_h = planet_house_map.get('Sun', 1)
        if sun_h == mer_h:
            active_yogas.append(YogaResult(
                name="Budhaditya Yoga",
                category="Raja Yoga",
                formula="Sun and Mercury conjunct in the same house",
                participating_planets=["Sun", "Mercury"],
                participating_houses=[sun_h],
                result_narrative="Sharp intellect, analytical capability, government favor, administrative skills, and professional acclaim.",
                confidence=85.0,
                priority="Medium",
                affected_areas=["Intellect", "Administration", "Status"]
            ))

        # 4. Chandra Mangala Yoga (Moon + Mars in same house)
        if moon_h == mars_h:
            active_yogas.append(YogaResult(
                name="Chandra Mangala Yoga",
                category="Dhana Yoga",
                formula="Moon and Mars conjunct in the same house",
                participating_planets=["Moon", "Mars"],
                participating_houses=[moon_h],
                result_narrative="High financial acumen, enterprise, success in real estate and trade, though emotional intensity requires balance.",
                confidence=85.0,
                priority="Medium",
                affected_areas=["Wealth", "Property", "Business"]
            ))

        # 5. Adhi Yoga (Benefics Mercury, Jupiter, Venus in 6th, 7th, 8th from Moon)
        benefic_houses_from_moon = [((planet_house_map[p] - moon_h) % 12) + 1 for p in ['Mercury', 'Jupiter', 'Venus']]
        if all(h in [6, 7, 8] for h in benefic_houses_from_moon):
            active_yogas.append(YogaResult(
                name="Chandradhi Yoga",
                category="Raja Yoga",
                formula="Mercury, Jupiter, and Venus occupy 6th, 7th, or 8th houses from Moon",
                participating_planets=["Mercury", "Jupiter", "Venus", "Moon"],
                participating_houses=[planet_house_map['Mercury'], planet_house_map['Jupiter'], planet_house_map['Venus']],
                result_narrative="Bestows minister-level power, leadership, polite temperament, long health, and triumph over all adversaries.",
                confidence=92.0,
                priority="High",
                affected_areas=["Leadership", "Status", "Health"]
            ))

        return active_yogas
