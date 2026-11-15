import math


def calibration_bins(probs: list[float], labels: list[int], n_bins: int = 10) -> list[tuple[int, float, float, int]]:
    if len(probs) != len(labels):
        raise ValueError("length mismatch")
    bins: dict[int, list[tuple[float, int]]] = {}
    for p, y in zip(probs, labels):
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"probability out of range: {p}")
        i = min(math.floor(p * n_bins), n_bins - 1)
        bins.setdefault(i, []).append((p, y))
    out = []
    for i in sorted(bins):
        items = bins[i]
        count = len(items)
        out.append((i, sum(p for p, _ in items) / count, sum(y for _, y in items) / count, count))
    return out
