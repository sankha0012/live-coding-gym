import math
def assign(orders, couriers):
    result = {}
    for oid, ox, oy in orders:
        if not couriers:
            result[oid] = None; continue
        best = min(couriers, key=lambda c: (math.dist((ox, oy), couriers[c]), c))
        result[oid] = best; del couriers[best]
    return result
