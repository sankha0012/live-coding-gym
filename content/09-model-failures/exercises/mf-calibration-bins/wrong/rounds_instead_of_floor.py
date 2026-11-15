def calibration_bins(probs, labels, n_bins=10):
    if len(probs) != len(labels):
        raise ValueError("x")
    bins = {}
    for p, y in zip(probs, labels):
        if not 0.0 <= p <= 1.0:
            raise ValueError
        i = min(int(round(p * n_bins)), n_bins - 1)
        bins.setdefault(i, []).append((p, y))
    return [(i, sum(p for p,_ in b)/len(b), sum(y for _,y in b)/len(b), len(b)) for i, b in sorted(bins.items())]
