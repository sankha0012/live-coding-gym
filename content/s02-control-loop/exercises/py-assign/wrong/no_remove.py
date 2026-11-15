import math
def assign(orders, couriers):
    result = {}
    for oid, ox, oy in orders:
        if not couriers:
            result[oid] = None; continue
        result[oid] = min(couriers, key=lambda c: (math.dist((ox, oy), couriers[c]), c))
    return result
