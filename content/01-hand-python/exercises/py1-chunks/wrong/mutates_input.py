def chunks(items, n):
    if n <= 0: raise ValueError
    out = []
    while items:
        out.append(items[:n]); del items[:n]
    return out
