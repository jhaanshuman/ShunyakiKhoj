from .aspects import has_jaimini_aspect

def calculate_raj_yogas(karakas, planet_signs):
    """
    Calculate Jaimini Raj Yogas based on Chara Karakas.
    karakas: dict mapping 'AK', 'AmK', etc to planet names
    planet_signs: dict mapping planet names to their signs
    """
    yogas = []
    
    # Check AK and AmK conjunction/aspect
    ak = karakas.get('AK')
    amk = karakas.get('AmK')
    pk = karakas.get('PK')
    dk = karakas.get('DK')
    
    pairs = [
        (ak, amk, "AK and AmK"),
        (ak, pk, "AK and PK"),
        (ak, dk, "AK and DK"),
        (amk, pk, "AmK and PK"),
        (amk, dk, "AmK and DK"),
        (pk, dk, "PK and DK")
    ]
    
    for p1, p2, name in pairs:
        if not p1 or not p2:
            continue
        sign1 = planet_signs.get(p1)
        sign2 = planet_signs.get(p2)
        if sign1 == sign2:
            yogas.append(f"{name} are conjunct in sign {sign1} (Jaimini Raj Yoga).")
        elif has_jaimini_aspect(sign1, sign2):
            yogas.append(f"{name} mutually aspect each other (Jaimini Raj Yoga).")
            
    return yogas
