def mean_valid(values):
    valid = [v for v in values if v is not None and v is not float("nan")]
    if not valid:
        return None
    return sum(valid) / len(valid)
