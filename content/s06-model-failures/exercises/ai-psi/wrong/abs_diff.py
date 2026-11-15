import math
def psi(expected, actual):
    total = 0.0
    for e, a in zip(expected, actual):
        e, a = max(e, 1e-4), max(a, 1e-4)
        total += abs(a - e) * math.log(a / e)
    return total
