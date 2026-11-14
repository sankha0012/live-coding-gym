def clamp(x, lo, hi):
    if lo > hi:
        lo, hi = hi, lo
    return max(lo, min(x, hi))
