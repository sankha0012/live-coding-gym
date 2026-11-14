def mean_valid(values):
    """Mean of the numbers in values, ignoring None and NaN.

    Zero counts as a valid value. Returns None if nothing valid is left.
    """
    valid = [v for v in values if v is not None and v != float("nan")]
    if not valid:
        return None
    return sum(valid) / len(valid)
