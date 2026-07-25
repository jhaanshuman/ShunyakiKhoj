# -*- coding: utf-8 -*-
"""
Divisional Engine: Mathematical calculation of all 20+ Divisional Charts (D1 to D144).
"""
from typing import Dict, Any, List, Tuple
from .planets import SIGN_NAMES

DIVISIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20, 24, 27, 30, 40, 45, 60, 81, 108, 144]

class DivisionalEngine:
    """Computes exact divisional positions for planets and ascendant across all Vargas."""
    
    @staticmethod
    def get_divisional_sign(lon: float, div: int) -> Tuple[str, float]:
        """
        Calculate sign name and degree within division for a given longitude and division factor.
        Returns: (sign_name, degree_in_div_sign)
        """
        lon = lon % 360.0
        sign_idx = int(lon // 30)
        sign_lon = lon % 30.0
        
        is_odd = (sign_idx % 2 == 0) # Aries=0 (odd), Taurus=1 (even)
        
        div_sign_idx = sign_idx
        
        if div == 1:
            div_sign_idx = sign_idx
        elif div == 2: # Hora
            # Odd sign: 0-15 Sun (Leo), 15-30 Moon (Cancer)
            # Even sign: 0-15 Moon (Cancer), 15-30 Sun (Leo)
            if is_odd:
                div_sign_idx = 4 if sign_lon < 15.0 else 3
            else:
                div_sign_idx = 3 if sign_lon < 15.0 else 4
        elif div == 3: # Drekkana
            part = int(sign_lon // 10.0)
            div_sign_idx = (sign_idx + part * 4) % 12
        elif div == 4: # Chaturthamsa
            part = int(sign_lon // 7.5)
            div_sign_idx = (sign_idx + part * 3) % 12
        elif div == 7: # Saptamsa
            part = int(sign_lon // (30.0 / 7.0))
            start_sign = sign_idx if is_odd else (sign_idx + 6) % 12
            div_sign_idx = (start_sign + part) % 12
        elif div == 9: # Navamsa
            part = int(sign_lon // (30.0 / 9.0))
            # Fire (0,4,8) -> Aries(0), Earth (1,5,9) -> Capricorn(9), Air (2,6,10) -> Libra(6), Water (3,7,11) -> Cancer(3)
            element = sign_idx % 4
            starts = [0, 9, 6, 3]
            div_sign_idx = (starts[element] + part) % 12
        elif div == 10: # Dasamsa
            part = int(sign_lon // 3.0)
            start_sign = sign_idx if is_odd else (sign_idx + 8) % 12
            div_sign_idx = (start_sign + part) % 12
        elif div == 12: # Dwadasamsa
            part = int(sign_lon // 2.5)
            div_sign_idx = (sign_idx + part) % 12
        elif div == 16: # Shodasamsa
            part = int(sign_lon // (30.0 / 16.0))
            # Movable -> Aries, Fixed -> Leo, Dual -> Sagittarius
            q = sign_idx % 3
            starts = [0, 4, 8]
            div_sign_idx = (starts[q] + part) % 12
        elif div == 20: # Vimsamsa
            part = int(sign_lon // 1.5)
            q = sign_idx % 3
            starts = [0, 8, 4]
            div_sign_idx = (starts[q] + part) % 12
        elif div == 24: # Chaturvimsamsa
            part = int(sign_lon // 1.25)
            start_sign = 4 if is_odd else 3 # Leo or Cancer
            div_sign_idx = (start_sign + part) % 12
        elif div == 27: # Saptavimsamsa (Nakshatramsa)
            part = int(sign_lon // (30.0 / 27.0))
            q = sign_idx % 4
            starts = [0, 3, 6, 9]
            div_sign_idx = (starts[q] + part) % 12
        elif div == 30: # Trimsamsa
            # Odd: 0-5 Mars(Aries), 5-10 Sat(Aquarius), 10-18 Jup(Sagittarius), 18-25 Mer(Gemini), 25-30 Ven(Libra)
            # Even: 0-5 Ven(Taurus), 5-12 Mer(Virgo), 12-20 Jup(Pisces), 20-25 Sat(Capricorn), 25-30 Mars(Scorpio)
            if is_odd:
                if sign_lon < 5.0: div_sign_idx = 0
                elif sign_lon < 10.0: div_sign_idx = 10
                elif sign_lon < 18.0: div_sign_idx = 8
                elif sign_lon < 25.0: div_sign_idx = 2
                else: div_sign_idx = 6
            else:
                if sign_lon < 5.0: div_sign_idx = 1
                elif sign_lon < 12.0: div_sign_idx = 5
                elif sign_lon < 20.0: div_sign_idx = 11
                elif sign_lon < 25.0: div_sign_idx = 9
                else: div_sign_idx = 7
        elif div == 40: # Khavedamsa
            part = int(sign_lon // 0.75)
            start_sign = 0 if is_odd else 6 # Aries or Libra
            div_sign_idx = (start_sign + part) % 12
        elif div == 45: # Akshavedamsa
            part = int(sign_lon // (30.0 / 45.0))
            q = sign_idx % 3
            starts = [0, 4, 8] # Movable Aries, Fixed Leo, Dual Sag
            div_sign_idx = (starts[q] + part) % 12
        elif div == 60: # Shastiamsa
            part = int(sign_lon // 0.5)
            div_sign_idx = (sign_idx + part) % 12
        else: # Generic fallback for D5, D6, D8, D11, D81, D108, D144
            part = int(sign_lon // (30.0 / div))
            div_sign_idx = (sign_idx + part) % 12
            
        div_size = 30.0 / div
        rem = sign_lon % div_size
        div_deg = round(rem * div, 2)
        
        return SIGN_NAMES[div_sign_idx % 12], div_deg, div_sign_idx % 12

    # 60 Shashtiamsa Deities (Parashari order)
    SHASTIAMSA_DEITIES = [
        "Ghor", "Rakshas", "Dev", "Kuber", "Yaksha", "Kinnar", "Bhrasht", "Kulaghn",
        "Garal", "Vagni", "Maya", "Pretapura", "Apampati", "Devat", "Amrit", "Chandra",
        "Vandana", "Nishachar", "Amrita", "Sudha", "Kala", "Dambha", "Kriti", "Kalyana",
        "Kalarnava", "Mukhya", "Shitla", "Sudha", "Pramida", "Yamya", "Kantikari", "Kala",
        "Davagni", "Ghor", "Yama", "Kantara", "Karakshya", "Chandra", "Amrita", "Sharama",
        "Durga", "Shubha", "Kshatriya", "Deva", "Vyas", "Vishna", "Prajapati", "Agni",
        "Yama", "Konnaga", "Shreeda", "Deva", "Amrita", "Katha", "Chandra", "Vardhamana",
        "Indra", "Mridu", "Varga", "Guru"
    ]

    SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
    EXALTATION_SIGNS = {'Sun': 0, 'Moon': 1, 'Mars': 9, 'Mercury': 5, 'Jupiter': 3, 'Venus': 11, 'Saturn': 6, 'Rahu': 1, 'Ketu': 7}
    DEBILITATION_SIGNS = {'Sun': 6, 'Moon': 7, 'Mars': 3, 'Mercury': 11, 'Jupiter': 9, 'Venus': 5, 'Saturn': 0, 'Rahu': 7, 'Ketu': 1}
    OWN_SIGNS = {
        'Sun': [4], 'Moon': [3], 'Mars': [0, 7], 'Mercury': [2, 5],
        'Jupiter': [8, 11], 'Venus': [1, 6], 'Saturn': [9, 10], 'Rahu': [10], 'Ketu': [7]
    }

    @classmethod
    def calculate_all_divisional_charts(
        cls,
        asc_sid_lon: float,
        planets_data: Dict[str, Any]
    ) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Compute all divisional charts for planets and Ascendant with dignities and D60 deities."""
        div_charts: Dict[str, Dict[str, Dict[str, Any]]] = {}
        
        # Track own sign/exalted counts per planet across the 10 major vargas for Vaisheshikamsa
        VAISESHIKAMSA_VARGAS = [1, 2, 3, 7, 9, 10, 12, 16, 30, 60]
        varga_dignity_counts = {p: 0 for p in planets_data.keys()}

        for div in DIVISIONS:
            div_key = f"D{div}"
            div_charts[div_key] = {}
            
            # Ascendant
            asc_sign, asc_deg, asc_s_idx = cls.get_divisional_sign(asc_sid_lon, div)
            div_charts[div_key]['Asc'] = {
                "sign": asc_sign,
                "sign_index": asc_s_idx,
                "sign_lord": cls.SIGN_LORDS[asc_s_idx],
                "lon": asc_deg,
                "house": 1
            }
            
            # Planets
            for p_name, p_obj in planets_data.items():
                p_lon = p_obj.sidereal_lon if hasattr(p_obj, 'sidereal_lon') else p_obj['sidereal_lon']
                p_sign, p_deg, p_s_idx = cls.get_divisional_sign(p_lon, div)
                
                # House in this divisional chart relative to div Ascendant
                v_house = ((p_s_idx - asc_s_idx + 12) % 12) + 1
                
                # Dignity state in this varga
                lord = cls.SIGN_LORDS[p_s_idx]
                if p_s_idx == cls.EXALTATION_SIGNS.get(p_name, -1):
                    dignity = "Exalted"
                elif p_s_idx == cls.DEBILITATION_SIGNS.get(p_name, -1):
                    dignity = "Debilitated"
                elif p_s_idx in cls.OWN_SIGNS.get(p_name, []):
                    dignity = "Own Sign"
                elif lord == p_name:
                    dignity = "Own Sign"
                else:
                    dignity = "Neutral"

                if div in VAISESHIKAMSA_VARGAS and dignity in ["Exalted", "Own Sign"]:
                    varga_dignity_counts[p_name] = varga_dignity_counts.get(p_name, 0) + 1

                p_dict = {
                    "sign": p_sign,
                    "sign_index": p_s_idx,
                    "sign_lord": lord,
                    "lon": p_deg,
                    "house": v_house,
                    "dignity": dignity
                }

                # Add D60 Shashtiamsa deity if D60
                if div == 60:
                    part = int((p_lon % 30.0) // 0.5)
                    # Odd sign: 1 to 60, Even sign: 60 to 1
                    is_odd = (int(p_lon // 30) % 2 == 0)
                    deity_idx = part if is_odd else (59 - part)
                    deity_name = cls.SHASTIAMSA_DEITIES[deity_idx % 60]
                    p_dict["shashtiamsa_deity"] = deity_name

                div_charts[div_key][p_name] = p_dict
                
        # Attach Vaisheshikamsa summary to metadata
        vaisheshikamsa_labels = {
            2: "Parijata", 3: "Uttama", 4: "Gopura", 5: "Simhasana",
            6: "Paravata", 7: "Devaloka", 8: "Kumkuma", 9: "Airavata", 10: "Brahmaloka"
        }
        div_charts["_vaisheshikamsa"] = {
            p: {
                "good_vargas_count": count,
                "classification": vaisheshikamsa_labels.get(count, "Ordinary" if count < 2 else "Brahmaloka")
            }
            for p, count in varga_dignity_counts.items()
        }

        return div_charts
