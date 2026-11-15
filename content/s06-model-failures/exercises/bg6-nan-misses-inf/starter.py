import math


def guard_scores(scores: list, fallback: float = 0.5) -> tuple[list[float], int]:
    clean, bad = [], 0
    for s in scores:
        ok = isinstance(s, (int, float)) and not isinstance(s, bool) and not math.isnan(s)
        if ok:
            clean.append(s)
        else:
            clean.append(fallback)
            bad += 1
    return clean, bad
