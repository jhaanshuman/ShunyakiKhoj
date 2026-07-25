def generate_graph_datasets(master_obj):
    """
    Generates JSON-ready datasets for charting libraries.
    Produces raw data structure, NEVER HTML/SVG/Images.
    """
    return {
        "planet_strength_radar": {
            "labels": ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"],
            "datasets": [
                {"label": "Shadbala", "data": [120, 110, 150, 100, 140, 90, 85]}
            ]
        },
        "dasha_timeline_gantt": {
            "rows": [
                {"lord": "Sun", "start_year": 2000, "end_year": 2006, "quality": "Good"},
                {"lord": "Moon", "start_year": 2006, "end_year": 2016, "quality": "Average"}
            ]
        },
        "house_strength_bar": {
            "labels": ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11", "H12"],
            "datasets": [
                {"label": "Strength", "data": [8, 5, 7, 6, 9, 4, 7, 3, 8, 9, 6, 4]}
            ]
        },
        "yoga_distribution_pie": {
            "labels": ["Raja", "Dhana", "Arishta"],
            "values": [3, 2, 1]
        },
        "dosha_severity_gauge": {
            "score": 65,
            "severity_label": "Moderate",
            "breakdown": ["Manglik: Low", "Kala Sarpa: None"]
        },
        "life_domain_radar": {
            "labels": ["Health", "Wealth", "Career", "Relationships", "Spirituality"],
            "datasets": [
                {"label": "Score", "data": [80, 70, 90, 60, 85]}
            ]
        },
        "planet_influence_network_d3": {
            "nodes": [
                {"id": "Sun", "name": "Sun", "type": "Planet", "strength": 120},
                {"id": "Moon", "name": "Moon", "type": "Planet", "strength": 110}
            ],
            "links": [
                {"source": "Sun", "target": "Moon", "relation": "Conjunction", "weight": 5}
            ]
        },
        "transit_intensity_heatmap": {
            "rows": ["Sun", "Moon", "Mars"],
            "cols": ["Jan", "Feb", "Mar"],
            "matrix": [[1, 2, 3], [3, 2, 1], [2, 3, 1]]
        }
    }
