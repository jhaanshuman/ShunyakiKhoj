def calculate_kp_significators(planets, house_cusps):
    """
    Compute KP House Significators.
    Level 1: Planet in Star of occupant
    Level 2: Occupant planet
    Level 3: Planet in Star of Lord
    Level 4: House Lord
    
    planets: dict with planet info including 'star_lord', 'house_occupying', 'houses_owned'
    house_cusps: dict mapping house to sign lord
    """
    significators = {i: {'L1': set(), 'L2': set(), 'L3': set(), 'L4': set()} for i in range(1, 13)}
    
    # Build maps
    occupants = {i: [] for i in range(1, 13)}
    for p, data in planets.items():
        house = data.get('house_occupying')
        if house:
            occupants[house].append(p)
            
    for house in range(1, 13):
        # Level 4: House Lord
        h_lord = house_cusps.get(house, {}).get('sign_lord')
        if h_lord:
            significators[house]['L4'].add(h_lord)
            
        # Level 2: Occupants
        occ = occupants[house]
        for p in occ:
            significators[house]['L2'].add(p)
            
    # Level 1 and 3 requires checking planets whose star lord is the Level 2 or Level 4
    for p, data in planets.items():
        sl = data.get('star_lord')
        if not sl:
            continue
            
        for house in range(1, 13):
            # Level 1: Planet whose star lord is an occupant (L2)
            if sl in significators[house]['L2']:
                significators[house]['L1'].add(p)
                
            # Level 3: Planet whose star lord is the house lord (L4)
            if sl in significators[house]['L4']:
                significators[house]['L3'].add(p)
                
    # Convert sets to sorted lists for deterministic output
    for house in range(1, 13):
        significators[house]['L1'] = sorted(list(significators[house]['L1']))
        significators[house]['L2'] = sorted(list(significators[house]['L2']))
        significators[house]['L3'] = sorted(list(significators[house]['L3']))
        significators[house]['L4'] = sorted(list(significators[house]['L4']))
        
    return significators
