import math


def guard_scores(scores: list, fallback: float = 0.5) -> tuple[list[float], int]:
    bad = 0
    for i, s in enumerate(scores):
        if not isinstance(s, (int, float)) or not math.isfinite(s):
            scores[i] = fallback
            bad += 1
    return scores, bad
