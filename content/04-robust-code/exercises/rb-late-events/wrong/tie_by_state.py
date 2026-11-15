def final_state(events):
    seen, uniq = set(), []
    for e in events:
        if e["id"] not in seen:
            seen.add(e["id"])
            uniq.append(e)
    best = {}
    for e in sorted(uniq, key=lambda e: (e["ts"], e["state"])):
        best[e["entity"]] = e["state"]
    return best
