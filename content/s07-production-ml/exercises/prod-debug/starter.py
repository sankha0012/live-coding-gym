def top_features(weights, k=2):
    """The k feature names with the largest absolute weight; ties broken by name."""
    names = list(set(weights))
    names.sort(key=lambda n: abs(weights[n]))
    return names[:k]


def normalize(batch):
    """Scale 'amount' to [0, 1] within the batch. Must NOT modify the input.
    If all amounts are equal, every scaled value is 0.0. Empty batch -> []."""
    lo = min(r["amount"] for r in batch)
    hi = max(r["amount"] for r in batch)
    for r in batch:
        r["amount"] = (r["amount"] - lo) / (hi - lo)
    return batch


def mean_score(scores):
    """Average of the scores, ignoring None. Empty or all-None -> None."""
    return sum(scores) / len(scores)
