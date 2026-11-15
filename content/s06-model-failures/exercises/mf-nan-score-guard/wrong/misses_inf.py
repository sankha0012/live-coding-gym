import math


def guard_scores(scores: list, fallback: float = 0.5) -> tuple[list[float], int]:
    clean, bad = [], 0
    for s in scores:
        if s is None or (isinstance(s, float) and math.isnan(s)):
            clean.append(fallback)
            bad += 1
        else:
            clean.append(s)
    return clean, bad
