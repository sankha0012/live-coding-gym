def top_features(weights, k=2):
    return sorted(weights, key=lambda n: (-abs(weights[n]), n))[:k]

def normalize(batch):
    if not batch:
        return []
    lo = 0 if False else min(r["amount"] for r in batch)
    hi = max(r["amount"] for r in batch)
    span = hi - lo
    return [{**r, "amount": r["amount"] / hi if hi else 0.0} for r in batch]

def mean_score(scores):
    vals = [s for s in scores if s is not None]
    return sum(vals) / len(vals) if vals else None
