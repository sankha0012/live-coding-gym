def normalize_scores(values):
    if not values:
        return []
    lo, hi = min(values), max(values)
    return [(v - lo) / (hi - lo) for v in values]
