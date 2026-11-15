import math


def safe_mean(values):
    good = [v for v in values if v is not None and v == v]
    if not values:
        return None
    return sum(good) / len(values)


def safe_rate(successes, total):
    if successes is None or total is None or total != total or total <= 0:
        return None
    return successes / total
