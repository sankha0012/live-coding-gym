def gmv_by_city(orders):
    out = {}
    for o in orders:
        out[o["city"]] = out.get(o["city"], 0) + (o["subtotal"] or 0) + o["fee"]
    return {c: round(v, 2) for c, v in out.items()}
