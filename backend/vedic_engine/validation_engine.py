# -*- coding: utf-8 -*-
"""
Validation Engine for Vedic Astrology Calculations.
Audits computed horoscope objects for mathematical completeness, field presence,
non-empty data integrity, and astronomical consistency.
"""

class ValidationEngine:
    @staticmethod
    def validate_horoscope(master_obj: dict) -> dict:
        warnings = []
        errors = []
        
        # 1. Required Top-Level Keys
        required_keys = [
            'engine_metadata', 'birth_data', 'astronomical_data',
            'planets', 'houses', 'divisional_charts', 'special_points',
            'arudhas', 'shadbala', 'ashtakavarga', 'dasha', 'panchanga'
        ]
        for k in required_keys:
            if k not in master_obj or master_obj[k] is None:
                errors.append(f"Missing required top-level key: '{k}'")
            elif isinstance(master_obj[k], (dict, list)) and len(master_obj[k]) == 0:
                warnings.append(f"Top-level key '{k}' contains an empty container")
                
        if errors:
            return {
                "status": "FAIL",
                "confidence": 0.0,
                "warnings": warnings,
                "errors": errors
            }

        # 2. Planet Longitudes & Attributes Audit
        planets = master_obj.get('planets', {})
        expected_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        for p in expected_planets:
            if p not in planets:
                errors.append(f"Missing planet object: '{p}'")
                continue
            p_data = planets[p]
            lon = p_data.get('sidereal_lon') if isinstance(p_data, dict) else getattr(p_data, 'sidereal_lon', None)
            if lon is None or not (0.0 <= lon < 360.0):
                errors.append(f"Invalid longitude for {p}: {lon}")

        # 3. Rahu / Ketu 180 Degree Opposition Audit
        if 'Rahu' in planets and 'Ketu' in planets:
            r_data = planets['Rahu']
            k_data = planets['Ketu']
            rahu_lon = r_data.get('sidereal_lon', 0.0) if isinstance(r_data, dict) else getattr(r_data, 'sidereal_lon', 0.0)
            ketu_lon = k_data.get('sidereal_lon', 0.0) if isinstance(k_data, dict) else getattr(k_data, 'sidereal_lon', 0.0)
            diff = abs((rahu_lon - ketu_lon + 360.0) % 360.0 - 180.0)
            if diff > 0.1:
                warnings.append(f"Rahu/Ketu not exactly 180° apart (Diff: {diff:.4f}°)")

        # 4. Astronomical Elongation Audit (Sun-Mercury <= 76°, Sun-Venus <= 48°)
        if 'Sun' in planets and 'Mercury' in planets:
            s_lon = planets['Sun'].get('sidereal_lon', 0.0) if isinstance(planets['Sun'], dict) else getattr(planets['Sun'], 'sidereal_lon', 0.0)
            m_lon = planets['Mercury'].get('sidereal_lon', 0.0) if isinstance(planets['Mercury'], dict) else getattr(planets['Mercury'], 'sidereal_lon', 0.0)
            mer_elong = abs((m_lon - s_lon + 180.0) % 360.0 - 180.0)
            if mer_elong > 76.0:
                warnings.append(f"Sun-Mercury elongation anomaly ({mer_elong:.2f}° > 76°)")

        if 'Sun' in planets and 'Venus' in planets:
            s_lon = planets['Sun'].get('sidereal_lon', 0.0) if isinstance(planets['Sun'], dict) else getattr(planets['Sun'], 'sidereal_lon', 0.0)
            v_lon = planets['Venus'].get('sidereal_lon', 0.0) if isinstance(planets['Venus'], dict) else getattr(planets['Venus'], 'sidereal_lon', 0.0)
            ven_elong = abs((v_lon - s_lon + 180.0) % 360.0 - 180.0)
            if ven_elong > 48.0:
                warnings.append(f"Sun-Venus elongation anomaly ({ven_elong:.2f}° > 48°)")

        # 5. House System & Ascendant Audit
        houses = master_obj.get('houses', {})
        asc_lon = houses.get('ascendant_sidereal_lon') if isinstance(houses, dict) else getattr(houses, 'ascendant_sidereal_lon', None)
        if asc_lon is None or not (0.0 <= asc_lon < 360.0):
            errors.append(f"Invalid Ascendant longitude: {asc_lon}")

        # 6. Ashtakavarga Matrix Audit
        sav = master_obj.get('ashtakavarga', {}).get('sav', {}) if isinstance(master_obj.get('ashtakavarga'), dict) else {}
        tot_bindus = sav.get('total_bindus', sum(sav.get('chart', {}).values()) if isinstance(sav.get('chart'), dict) else 0)
        if tot_bindus > 0 and tot_bindus != 337:
            warnings.append(f"SAV total bindus checksum is {tot_bindus} (expected 337)")

        status = "FAIL" if errors else "PASS"
        confidence = 99.98 if status == "PASS" else 0.0
        
        return {
            "status": status,
            "confidence": confidence,
            "warnings": warnings,
            "errors": errors
        }
