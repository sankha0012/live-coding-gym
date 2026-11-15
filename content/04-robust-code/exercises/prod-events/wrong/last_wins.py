def apply_events(events):
    seen, out, dupes = set(), {}, 0
    for e in events:
        if e["event_id"] in seen:
            dupes += 1
            continue
        seen.add(e["event_id"])
        out[e["order_id"]] = e["status"]
    return out, dupes
