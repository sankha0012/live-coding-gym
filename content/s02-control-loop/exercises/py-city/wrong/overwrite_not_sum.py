def gmv_by_city(orders):
    out = {}
    for o in orders:
        if o["status"] != "delivered": continue
        out[o["city"]] = round((o["subtotal"] or 0) + o["fee"], 2)
    return out
