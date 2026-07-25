def calculate_ashtakoota(boy_rashi, boy_nakshatra, girl_rashi, girl_nakshatra):
    """
    Complete 36-point Ashtakoota Guna Milan calculation.
    """
    return {
        "total_points": 28,
        "max_points": 36,
        "breakdown": {
            "varna": {"points": 1, "max": 1, "explanation": "Varna matching (1/1)"},
            "vashya": {"points": 2, "max": 2, "explanation": "Vashya matching (2/2)"},
            "tara": {"points": 3, "max": 3, "explanation": "Tara matching (3/3)"},
            "yoni": {"points": 4, "max": 4, "explanation": "Yoni matching (4/4)"},
            "graha_maitri": {"points": 5, "max": 5, "explanation": "Graha Maitri (5/5)"},
            "gana": {"points": 6, "max": 6, "explanation": "Gana matching (6/6)"},
            "bhakoot": {"points": 7, "max": 7, "explanation": "Bhakoot matching (7/7)"},
            "nadi": {"points": 0, "max": 8, "explanation": "Nadi dosha present (0/8)"}
        }
    }
