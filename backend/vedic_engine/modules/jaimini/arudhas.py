def calculate_arudha_padas(houses, lords_positions):
    """
    Calculate Arudha Padas for all 12 houses.
    houses: list of house signs (1-12)
    lords_positions: dict mapping sign to its lord's sign
                     e.g. {1: 5} means lord of Aries is in Leo
    
    For Scorpio and Aquarius, stronger lord rule should be evaluated before passing lords_positions,
    but we will fallback to standard Mars/Saturn if Ketu/Rahu is not evaluated.
    """
    arudhas = {}
    for i in range(1, 13):
        house_sign = houses[i-1]
        lord_sign = lords_positions.get(house_sign, house_sign)
        
        # Calculate distance from house to lord (inclusive)
        distance = (lord_sign - house_sign) % 12
        
        # Arudha is distance away from lord
        arudha_sign = (lord_sign + distance) % 12
        if arudha_sign == 0:
            arudha_sign = 12
            
        # Exception Rules
        # If Pada falls in 1st from House, it goes to 10th
        if arudha_sign == house_sign:
            arudha_sign = (house_sign + 9) % 12
            if arudha_sign == 0: arudha_sign = 12
            
        # If Pada falls in 7th from House, it goes to 4th
        elif arudha_sign == (house_sign + 6) % 12 or arudha_sign == (house_sign - 6) % 12:
            arudha_sign = (house_sign + 3) % 12
            if arudha_sign == 0: arudha_sign = 12
            
        arudhas[f'A{i}'] = arudha_sign
        
    arudhas['AL'] = arudhas['A1']
    arudhas['UL'] = arudhas['A12']
    return arudhas
