import math


def _ok(v):
    return v is not None and not (isinstance(v, float) and math.isnan(v))


def safe_mean(values):
    good = [v for v in values if _ok(v)]
    if not good or not any(good):
        return None
    return sum(good) / len(good)


def safe_rate(successes, total):
    if not _ok(successes) or not _ok(total) or total <= 0:
        return None
    return successes / total
