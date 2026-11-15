def gmv_by_city(orders):
    out = {}
    for o in orders:
        if o["status"] != "delivered": continue
        out[o["city"]] = out.get(o["city"], 0) + (o["subtotal"] or 0) + o["fee"]
    return out
