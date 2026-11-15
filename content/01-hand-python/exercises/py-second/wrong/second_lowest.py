def second_highest(values):
    d = sorted(set(values))
    return d[1] if len(d) >= 2 else None
