events = [
    {"id": "e1", "user": "a", "amount": 10},
    {"id": "e2", "user": "b", "amount": 25},
    {"id": "e1", "user": "a", "amount": 10},
    {"id": "e3", "user": "a", "amount": 5},
    {"id": "e2", "user": "b", "amount": 25},
]

naive = {}
for ev in events:
    naive[ev["user"]] = naive.get(ev["user"], 0) + ev["amount"]
print("naive:", naive)

seen = set()
safe = {}
for ev in events:
    if ev["id"] in seen:
        continue
    seen.add(ev["id"])
    safe[ev["user"]] = safe.get(ev["user"], 0) + ev["amount"]
print("deduped:", safe)
print("dropped:", len(events) - len(seen))
