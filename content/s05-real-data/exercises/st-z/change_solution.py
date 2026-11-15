import math

def two_prop_z(x1, n1, x2, n2, pooled=True):
    p1, p2 = x1 / n1, x2 / n2
    if pooled:
        p = (x1 + x2) / (n1 + n2)
        se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    else:
        se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return (p2 - p1) / se
