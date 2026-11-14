import math


def mean_valid(values):
    valid = [v for v in values if v and not math.isnan(v)]
    if not valid:
        return None
    return sum(valid) / len(valid)
