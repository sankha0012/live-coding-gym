def clamp(x, lo, hi):
    if lo >= hi:
        raise ValueError("lo must be smaller than hi")
    return max(lo, min(x, hi))
