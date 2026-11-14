import math


def calibration_bins(probs, labels, n_bins=10):
    if len(probs) != len(labels):
        raise ValueError("length mismatch")
    bins = {}
    for p, y in zip(probs, labels):
        if not 0.0 <= p <= 1.0:
            raise ValueError("range")
        bins.setdefault(math.floor(p * n_bins), []).append((p, y))
    return [(i, sum(p for p, _ in v) / len(v), sum(y for _, y in v) / len(v), len(v))
            for i, v in sorted(bins.items())]
