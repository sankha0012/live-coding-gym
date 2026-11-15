def score(preds, golds, cats):
    norm = lambda s: s.strip().lower()
    hits, totals = {}, {}
    for p, g, c in zip(preds, golds, cats):
        hits[c] = hits.get(c, 0) + (norm(p) == norm(g))
        totals[c] = totals.get(c, 0) + 1
    if not totals:
        return {"overall": 0.0}
    out = {c: hits[c] / totals[c] for c in totals}
    out["overall"] = sum(out.values()) / len(out)
    return out
