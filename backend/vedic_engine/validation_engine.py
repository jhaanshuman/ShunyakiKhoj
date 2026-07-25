# -*- coding: utf-8 -*-
"""
Validation Engine for Vedic Astrology Calculations.
Audits computed horoscope objects for mathematical completeness, field presence,
and astronomical consistency before predictions are generated.
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
                
        if errors:
            return {
                "status": "FAIL",
                "confidence": 0.0,
                "warnings": warnings,
                "errors": errors
            }

        # 2. Planet Longitudes & Attributes
        planets = master_obj.get('planets', {})
        expected_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        for p in expected_planets:
            if p not in planets:
                errors.append(f"Missing planet object: '{p}'")
                continue
            p_data = planets[p]
            lon = p_data.get('sidereal_lon')
            if lon is None or not (0.0 <= lon < 360.0):
                errors.append(f"Invalid longitude for {p}: {lon}")
            sign_idx = p_data.get('sign_index')
            if sign_idx is None or not (0 <= sign_idx <= 11):
                errors.append(f"Invalid sign_index for {p}: {sign_idx}")
            nak_idx = p_data.get('nakshatra_index')
            if nak_idx is None or not (0 <= nak_idx <= 26):
                errors.append(f"Invalid nakshatra_index for {p}: {nak_idx}")
            pada = p_data.get('pada')
            if pada is None or not (1 <= pada <= 4):
                errors.append(f"Invalid pada for {p}: {pada}")

        # 3. Rahu / Ketu 180 Degree Opposition Audit
        if 'Rahu' in planets and 'Ketu' in planets:
            rahu_lon = planets['Rahu'].get('sidereal_lon', 0.0)
            ketu_lon = planets['Ketu'].get('sidereal_lon', 0.0)
            diff = abs((rahu_lon - ketu_lon + 360.0) % 360.0 - 180.0)
            if diff > 0.05:
                warnings.append(f"Rahu/Ketu not exactly 180° apart (Diff: {diff:.4f}°)")

        # 4. House System & Ascendant Audit
        houses = master_obj.get('houses', {})
        asc_lon = houses.get('ascendant_sidereal_lon')
        if asc_lon is None or not (0.0 <= asc_lon < 360.0):
            errors.append(f"Invalid Ascendant longitude: {asc_lon}")
            
        cusps = houses.get('cusps', [])
        if len(cusps) != 12:
            errors.append(f"Expected 12 house cusps, found {len(cusps)}")

        # 5. Divisional Charts Consistency Audit
        vargas = master_obj.get('divisional_charts', {})
        required_vargas = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60', 'D81', 'D108', 'D144']
        for v in required_vargas:
            if v not in vargas or not isinstance(vargas[v], dict):
                warnings.append(f"Divisional chart {v} missing or incomplete")

        # 6. Ashtakavarga Matrix Audit
        sav = master_obj.get('ashtakavarga', {}).get('sav', {})
        tot_bindus = sav.get('total_bindus', sum(sav.get('chart', {}).values()))
        if tot_bindus != 337:
            warnings.append(f"SAV total bindus checksum is {tot_bindus} (expected 337)")

        status = "FAIL" if errors else "PASS"
        confidence = 99.98 if status == "PASS" else 0.0
        
        return {
            "status": status,
            "confidence": confidence,
            "warnings": warnings,
            "errors": errors
        }
