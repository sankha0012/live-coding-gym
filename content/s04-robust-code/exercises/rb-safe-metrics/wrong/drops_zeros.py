import math


def safe_mean(values):
    good = [v for v in values if v and not math.isnan(v)]
    if not good:
        return None
    return sum(good) / len(good)


def safe_rate(successes, total):
    if not total or total < 0 or successes is None:
        return None
    return successes / total
