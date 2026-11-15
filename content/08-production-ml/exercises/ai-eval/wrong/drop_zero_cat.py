def score(preds, golds, cats):
    norm = lambda s: s.strip().lower()
    hits, totals = {}, {}
    for p, g, c in zip(preds, golds, cats):
        if norm(p) == norm(g):
            hits[c] = hits.get(c, 0) + 1
        totals[c] = totals.get(c, 0) + 1
    n = sum(totals.values())
    out = {"overall": (sum(hits.values()) / n) if n else 0.0}
    for c in hits:
        out[c] = hits[c] / totals[c]
    return out
