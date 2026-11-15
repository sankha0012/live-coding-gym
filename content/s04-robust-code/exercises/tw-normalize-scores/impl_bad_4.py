def normalize_scores(values):
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0] * len(values)
    values[:] = [(v - lo) / (hi - lo) for v in values]
    return values
