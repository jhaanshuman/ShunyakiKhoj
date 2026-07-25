def get_jaimini_aspects():
    """
    Returns a dictionary mapping a sign (1-12) to the signs it aspects in Jaimini.
    Movable (1,4,7,10) aspect Fixed except adjacent.
    Fixed (2,5,8,11) aspect Movable except adjacent.
    Dual (3,6,9,12) aspect other Dual signs.
    """
    return {
        1: [5, 8, 11],
        2: [4, 7, 10],
        3: [6, 9, 12],
        4: [2, 8, 11],
        5: [1, 7, 10],
        6: [3, 9, 12],
        7: [2, 5, 11],
        8: [1, 4, 10],
        9: [3, 6, 12],
        10: [2, 5, 8],
        11: [1, 4, 7],
        12: [3, 6, 9]
    }

def has_jaimini_aspect(sign1, sign2):
    aspects = get_jaimini_aspects()
    return sign2 in aspects.get(sign1, [])
