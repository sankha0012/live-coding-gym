import math


def safe_mean(values):
    good = [v for v in values if v is not None and not math.isnan(v)]
    if not good:
        return None
    return sum(good) / len(good)


def safe_rate(successes, total):
    if total is None or successes is None or total <= 0:
        return 0.0
    return successes / total
