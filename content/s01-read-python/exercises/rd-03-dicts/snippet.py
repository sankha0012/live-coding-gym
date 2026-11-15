events = ["click", "view", "click", "buy", "view", "click"]
limits = {"click": 2, "view": 5}

counts = {}
for event in events:
    counts[event] = counts.get(event, 0) + 1

print(counts)
for name, n in counts.items():
    limit = limits.get(name, 1)
    print(name, n, "over" if n > limit else "ok")

print(limits.get("scroll"))
print(sorted(counts, key=counts.get, reverse=True))
