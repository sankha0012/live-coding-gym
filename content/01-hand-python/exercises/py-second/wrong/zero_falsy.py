def second_highest(values):
    d = sorted(set(values), reverse=True)
    return d[1] if len(d) >= 2 and d[1] else None
