import math
def mean_valid(values):
    valid=[v for v in values if v is not None and not math.isnan(v)]
    return sum(valid)/len(values) if valid else None
