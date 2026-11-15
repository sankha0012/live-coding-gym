def apply_events(events):
    seen, best, dupes = set(), {}, 0
    for e in events:
        if e["event_id"] in seen:
            dupes += 1
            continue
        seen.add(e["event_id"])
        cur = best.get(e["order_id"])
        if cur is None or e["ts"] > cur[0]:
            best[e["order_id"]] = (e["ts"], e["status"])
    return {oid: s for oid, (_, s) in best.items()}, dupes
