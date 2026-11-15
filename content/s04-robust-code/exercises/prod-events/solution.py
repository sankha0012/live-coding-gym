def apply_events(events):
    seen, best, dupes = set(), {}, 0
    for e in events:
        if e["event_id"] in seen:
            dupes += 1
            continue
        seen.add(e["event_id"])
        key = (e["ts"], e["event_id"])
        cur = best.get(e["order_id"])
        if cur is None or key > cur[0]:
            best[e["order_id"]] = (key, e["status"])
    return {oid: status for oid, (_, status) in best.items()}, dupes
