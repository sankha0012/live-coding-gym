def average_delivery_minutes(orders):
    d = [o["actual_minutes"] for o in orders if o["status"] == "delivered"]
    if not d:
        return None
    return sum(d) / len(orders)
