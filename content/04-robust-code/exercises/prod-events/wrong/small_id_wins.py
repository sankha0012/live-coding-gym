def apply_events(events):
    seen, best, dupes = set(), {}, 0
    for e in events:
        if e["event_id"] in seen:
            dupes += 1
            continue
        seen.add(e["event_id"])
        cur = best.get(e["order_id"])
        if cur is None or e["ts"] > cur[0] or (e["ts"] == cur[0] and e["event_id"] < cur[1]):
            best[e["order_id"]] = (e["ts"], e["event_id"], e["status"])
    return {oid: v[2] for oid, v in best.items()}, dupes
