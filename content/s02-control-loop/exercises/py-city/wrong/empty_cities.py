def gmv_by_city(orders):
    out = {}
    for o in orders:
        out.setdefault(o["city"], 0)
        if o["status"] != "delivered": continue
        out[o["city"]] += (o["subtotal"] or 0) + o["fee"]
    return {c: round(v, 2) for c, v in out.items()}
