def latest_status(events):
    out = {}
    for oid, ts, s in events:
        out[oid] = max(out.get(oid, s), s)
    return out
