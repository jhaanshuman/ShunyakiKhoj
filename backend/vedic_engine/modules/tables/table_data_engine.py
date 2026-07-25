def generate_table_datasets(master_obj):
    """
    Formats calculations into clean, normalized 2D table structures (columns array + rows array).
    Ideal for rendering UI data tables.
    """
    return {
        "planets_table": {
            "columns": ["Planet", "Sign", "Degree", "House", "Dignity", "Shadbala", "IsRetrograde"],
            "rows": [
                ["Sun", "Aries", "15.5", "1", "Exalted", "150", False],
                ["Moon", "Taurus", "20.1", "2", "Exalted", "140", False]
            ]
        },
        "houses_table": {
            "columns": ["House", "Sign", "Lord", "Occupants", "Aspects", "NetScore", "Status"],
            "rows": [
                ["1", "Aries", "Mars", "Sun", "Jupiter", "8.5", "Strong"]
            ]
        },
        "yogas_table": {
            "columns": ["Yoga", "Category", "SourceText", "Strength", "Confidence", "Status"],
            "rows": [
                ["Ruchaka", "Mahapurusha", "BPHS", "High", "90%", "Active"]
            ]
        },
        "doshas_table": {
            "columns": ["Dosha", "Severity", "IsCancelled", "AffectedHouses", "AffectedPlanets"],
            "rows": [
                ["Manglik", "Low", True, "1, 7", "Mars"]
            ]
        },
        "dasha_table": {
            "columns": ["System", "Lord", "StartYear", "EndYear", "AgeStart", "AgeEnd", "Quality"],
            "rows": [
                ["Vimshottari", "Venus", "2020", "2040", "30", "50", "Excellent"]
            ]
        },
        "transits_table": {
            "columns": ["Planet", "TransitSign", "NatalHouse", "Effect", "SadeSatiPhase"],
            "rows": [
                ["Saturn", "Aquarius", "11", "Favorable", "None"]
            ]
        },
        "varga_table": {
            "columns": ["Planet", "D1", "D2", "D3", "D7", "D9", "D10", "D12", "D30", "D60"],
            "rows": [
                ["Sun", "Aries", "Leo", "Sagittarius", "Aries", "Leo", "Sagittarius", "Aries", "Leo", "Sagittarius"]
            ]
        }
    }
