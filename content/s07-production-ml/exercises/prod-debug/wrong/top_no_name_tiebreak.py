def top_features(weights, k=2):
    return sorted(weights, key=lambda n: -abs(weights[n]))[:k]

def normalize(batch):
    if not batch:
        return []
    lo = min(r["amount"] for r in batch)
    hi = max(r["amount"] for r in batch)
    span = hi - lo
    return [{**r, "amount": (r["amount"] - lo) / span if span else 0.0} for r in batch]

def mean_score(scores):
    vals = [s for s in scores if s is not None]
    return sum(vals) / len(vals) if vals else None
