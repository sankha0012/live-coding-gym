import math
def assign(orders, couriers):
    free = dict(couriers); result = {}
    for oid, ox, oy in orders:
        if not free:
            result[oid] = None; continue
        best = min(free, key=lambda c: math.dist((ox, oy), free[c]))
        result[oid] = best; del free[best]
    return result
