# (arrival order, event_time, user, status)
stream = [
    (1, 100, "u1", "created"),
    (2, 130, "u1", "paid"),
    (3, 110, "u1", "shipped"),   # arrives late: happened before "paid"
    (4, 120, "u2", "created"),
]

by_arrival = {}
for _, ts, user, status in sorted(stream, key=lambda e: e[1]):
    by_arrival[user] = status

by_event_time = {}
last_ts = {}
late = 0
for _, ts, user, status in stream:
    if ts >= last_ts.get(user, -1):
        by_event_time[user] = status
        last_ts[user] = ts
    else:
        late += 1

print("arrival:   ", sorted(by_arrival.items()))
print("event time:", sorted(by_event_time.items()))
print("dropped as late:", late)
