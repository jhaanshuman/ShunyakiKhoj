def calculate_ruling_planets(lagna_lords, moon_lords, day_lord):
    """
    Calculate KP Ruling Planets.
    lagna_lords: dict with 'star_lord', 'sign_lord'
    moon_lords: dict with 'star_lord', 'sign_lord'
    day_lord: string (planet of the weekday)
    """
    ruling_planets = {
        'lagna_star_lord': lagna_lords.get('star_lord'),
        'lagna_sign_lord': lagna_lords.get('sign_lord'),
        'moon_star_lord': moon_lords.get('star_lord'),
        'moon_sign_lord': moon_lords.get('sign_lord'),
        'day_lord': day_lord
    }
    
    # List in order of strength
    rp_list = [
        ruling_planets['lagna_star_lord'],
        ruling_planets['lagna_sign_lord'],
        ruling_planets['moon_star_lord'],
        ruling_planets['moon_sign_lord'],
        ruling_planets['day_lord']
    ]
    
    # Deduplicate while preserving order
    dedup = []
    for p in rp_list:
        if p and p not in dedup:
            dedup.append(p)
            
    ruling_planets['strongest_to_weakest'] = dedup
    
    return ruling_planets
