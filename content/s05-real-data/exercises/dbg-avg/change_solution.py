def average_delivery_minutes(orders, max_minutes=None):
    d = [o["actual_minutes"] for o in orders
         if o["status"] == "delivered" and o["actual_minutes"] is not None
         and (max_minutes is None or o["actual_minutes"] <= max_minutes)]
    if not d:
        return None
    return sum(d) / len(d)
