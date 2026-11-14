def average_delivery_minutes(orders):
    """Average actual_minutes over delivered orders. Return None if there are none."""
    total = 0
    for o in orders:
        total += o["actual_minutes"] or 0
    return total / len(orders)

O = [
    {"status": "delivered", "actual_minutes": 25},
    {"status": "delivered", "actual_minutes": 35},
    {"status": "cancelled", "actual_minutes": None},
]
print(average_delivery_minutes(O))
