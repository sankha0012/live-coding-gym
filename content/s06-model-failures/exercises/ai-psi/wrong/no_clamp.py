import math
def psi(expected, actual):
    total = 0.0
    for e, a in zip(expected, actual):
        if e == 0 or a == 0:
            continue
        total += (a - e) * math.log(a / e)
    return total
