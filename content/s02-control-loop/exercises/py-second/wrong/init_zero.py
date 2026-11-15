def second_highest(values):
    a = b = 0
    for v in values:
        if v > a: a, b = v, a
        elif v > b and v != a: b = v
    return b if b else None
