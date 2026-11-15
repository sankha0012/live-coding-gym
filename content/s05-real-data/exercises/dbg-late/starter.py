def late_rate(orders):
    d = [o for o in orders if o["status"] == "delivered"]
    late = [o for o in d if o["actual_minutes"] >= o["promised_minutes"]]
    return len(late) / len(d)

O = [
    {"status": "delivered", "promised_minutes": 30, "actual_minutes": 30},
    {"status": "delivered", "promised_minutes": 30, "actual_minutes": 45},
    {"status": "cancelled", "promised_minutes": 40, "actual_minutes": None},
]
print(late_rate(O))
