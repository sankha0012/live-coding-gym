def second_highest(values):
    values.sort(reverse=True)
    d = []
    for v in values:
        if v not in d: d.append(v)
    return d[1] if len(d) >= 2 else None
