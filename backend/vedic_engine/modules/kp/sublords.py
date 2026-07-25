# Vimshottari dasha lords sequence and their proportions (years)
DASHA_LORDS = [
    ('Ketu', 7),
    ('Venus', 20),
    ('Sun', 6),
    ('Moon', 10),
    ('Mars', 7),
    ('Rahu', 18),
    ('Jupiter', 16),
    ('Saturn', 19),
    ('Mercury', 17)
]
TOTAL_YEARS = 120.0
NAKSHATRA_DEG = 13.0 + 20.0/60.0 # 13.333333 deg

def get_sublords(longitude):
    """
    Calculate Sign Lord, Star Lord, Sub Lord, Sub-Sub Lord for a given longitude.
    """
    lon = longitude % 360
    
    # 1. Sign Lord (Simple mapping based on sign 1-12)
    sign = int(lon // 30) + 1
    sign_lords = {
        1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon', 5: 'Sun', 6: 'Mercury',
        7: 'Venus', 8: 'Mars', 9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
    }
    sign_lord = sign_lords[sign]
    
    # 2. Star Lord
    nak_idx = int(lon // NAKSHATRA_DEG)
    star_lord_idx = nak_idx % 9
    star_lord = DASHA_LORDS[star_lord_idx][0]
    
    # 3. Sub Lord
    rem_deg = lon % NAKSHATRA_DEG
    current_idx = star_lord_idx
    sub_lord = None
    accumulated_deg = 0.0
    
    for _ in range(9):
        lord, years = DASHA_LORDS[current_idx]
        span = (years / TOTAL_YEARS) * NAKSHATRA_DEG
        accumulated_deg += span
        if rem_deg <= accumulated_deg:
            sub_lord = lord
            break
        current_idx = (current_idx + 1) % 9
        
    # 4. Sub-Sub Lord (further subdivision of the sub lord span)
    # We subtract the previous accumulated_deg to get remainder within the sub lord span
    sub_rem_deg = rem_deg - (accumulated_deg - span)
    sub_sub_lord = None
    sub_accumulated_deg = 0.0
    
    ss_idx = DASHA_LORDS.index((sub_lord, [y for l,y in DASHA_LORDS if l == sub_lord][0]))
    for _ in range(9):
        lord, years = DASHA_LORDS[ss_idx]
        # proportional span of the sub-sub lord within the sub lord's span
        ss_span = (years / TOTAL_YEARS) * span
        sub_accumulated_deg += ss_span
        if sub_rem_deg <= sub_accumulated_deg:
            sub_sub_lord = lord
            break
        ss_idx = (ss_idx + 1) % 9
        
    return {
        'sign_lord': sign_lord,
        'star_lord': star_lord,
        'sub_lord': sub_lord,
        'sub_sub_lord': sub_sub_lord
    }
