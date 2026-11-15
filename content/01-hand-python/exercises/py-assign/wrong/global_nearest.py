import math
def assign(orders, couriers):
    free = dict(couriers); result = {o[0]: None for o in orders}
    pending = list(orders)
    while pending and free:
        d, c, o = min(((math.dist((o[1], o[2]), free[c]), c, o) for o in pending for c in free), key=lambda t: (t[0], t[1]))
        result[o[0]] = c; del free[c]; pending.remove(o)
    return result
