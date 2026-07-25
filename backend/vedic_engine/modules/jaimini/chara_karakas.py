def calculate_chara_karakas(planets, use_eight=False):
    """
    Calculate Jaimini Chara Karakas.
    planets: dict of planet data with 'lon' (longitude 0-360)
    use_eight: boolean, if True includes Rahu for 8 Karakas scheme (Pitrukaraka)
    """
    valid_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    if use_eight:
        valid_planets.append('Rahu')
        
    karaka_candidates = []
    for p in valid_planets:
        if p not in planets:
            continue
        lon = planets[p].get('sidereal_lon', planets[p].get('lon', 0.0))
        # Rahu's longitude is counted in reverse from end of sign
        if p == 'Rahu':
            deg_in_sign = 30.0 - (lon % 30)
        else:
            deg_in_sign = lon % 30
            
        karaka_candidates.append({
            'planet': p,
            'deg': deg_in_sign
        })
        
    # Sort descending by degree in sign
    karaka_candidates.sort(key=lambda x: x['deg'], reverse=True)
    
    karakas = {}
    if use_eight and len(karaka_candidates) >= 8:
        labels = ['AK', 'AmK', 'BK', 'MK', 'PiK', 'PK', 'GK', 'DK']
    else:
        labels = ['AK', 'AmK', 'BK', 'MK', 'PK', 'GK', 'DK']
        
    for i, candidate in enumerate(karaka_candidates[:len(labels)]):
        karakas[labels[i]] = candidate['planet']
        
    return karakas
