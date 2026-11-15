def clamp(x, lo, hi):
    if lo > hi:
        raise ValueError("lo must not be greater than hi")
    return min(x, hi)
