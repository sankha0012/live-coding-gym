def assign(orders, couriers):
    free = dict(couriers); result = {}
    for oid, ox, oy in orders:
        if not free:
            result[oid] = None; continue
        best = min(free, key=lambda c: (abs(ox-free[c][0])+abs(oy-free[c][1]), c))
        result[oid] = best; del free[best]
    return result
