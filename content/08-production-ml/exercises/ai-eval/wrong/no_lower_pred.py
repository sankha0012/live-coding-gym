def score(preds, golds, cats):
    hits, totals = {}, {}
    for p, g, c in zip(preds, golds, cats):
        ok = p.strip() == g.strip().lower()
        hits[c] = hits.get(c, 0) + ok
        totals[c] = totals.get(c, 0) + 1
    n = sum(totals.values())
    out = {"overall": (sum(hits.values()) / n) if n else 0.0}
    for c in totals:
        out[c] = hits[c] / totals[c]
    return out
