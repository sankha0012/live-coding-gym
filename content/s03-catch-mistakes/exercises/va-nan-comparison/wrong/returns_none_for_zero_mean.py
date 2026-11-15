import math
def mean_valid(values):
    valid=[v for v in values if v is not None and v==v]
    return (sum(valid)/len(valid)) or None if valid else None
