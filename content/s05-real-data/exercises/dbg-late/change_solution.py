def late_rate(orders, grace=0):
    d = [o for o in orders if o["status"] == "delivered"]
    if not d:
        return 0.0
    late = [o for o in d if o["actual_minutes"] > o["promised_minutes"] + grace]
    return len(late) / len(d)
