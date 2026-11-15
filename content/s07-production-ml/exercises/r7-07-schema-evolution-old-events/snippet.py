events = [
    {"v": 1, "user": "a", "amount": 12.5},
    {"v": 1, "user": "b", "amount": 7.0},
    {"v": 2, "user": "a", "amount_cents": 1000},
    {"v": 2, "user": "c", "amount_cents": 250},
]

total_cents = sum(e.get("amount_cents", 0) for e in events)
print(total_cents)
print(total_cents / 100)
print(len(events))
print(sum(1 for e in events if "amount_cents" not in e))
