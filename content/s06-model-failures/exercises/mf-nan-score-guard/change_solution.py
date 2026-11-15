import math


def guard_scores(scores: list, fallback: float = 0.5, lo=None, hi=None) -> tuple[list[float], int]:
    clean, bad = [], 0
    for s in scores:
        ok = isinstance(s, (int, float)) and not isinstance(s, bool) and math.isfinite(s)
        if ok and lo is not None and s < lo:
            ok = False
        if ok and hi is not None and s > hi:
            ok = False
        if ok:
            clean.append(s)
        else:
            clean.append(fallback)
            bad += 1
    return clean, bad
