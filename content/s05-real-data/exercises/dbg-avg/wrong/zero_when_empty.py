def average_delivery_minutes(orders):
    d = [o["actual_minutes"] for o in orders
         if o["status"] == "delivered" and o["actual_minutes"] is not None]
    if not d:
        return 0
    return sum(d) / len(d)
