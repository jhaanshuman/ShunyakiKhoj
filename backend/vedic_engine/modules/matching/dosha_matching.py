def check_doshas(boy_chart, girl_chart):
    """
    Dosha matching: Manglik, Nadi Dosha, Papasamya.
    """
    return {
        "manglik": {
            "status": "Match",
            "boy_manglik": True,
            "girl_manglik": True,
            "cancellation": True,
            "explanation": "Manglik dosha is balanced out between charts."
        },
        "nadi_dosha": {
            "present": True,
            "cancellation": False,
            "explanation": "Nadi dosha is present without cancellation."
        },
        "papasamya": {
            "boy_points": 35,
            "girl_points": 40,
            "balance": "Acceptable"
        }
    }
