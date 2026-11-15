def apply_events(events):
    seen, dup_ids, best = set(), set(), {}
    for e in events:
        if e["event_id"] in seen:
            dup_ids.add(e["event_id"])
            continue
        seen.add(e["event_id"])
        key = (e["ts"], e["event_id"])
        cur = best.get(e["order_id"])
        if cur is None or key > cur[0]:
            best[e["order_id"]] = (key, e["status"])
    return {oid: s for oid, (_, s) in best.items()}, len(dup_ids)
