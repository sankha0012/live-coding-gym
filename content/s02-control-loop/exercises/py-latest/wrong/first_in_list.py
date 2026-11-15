def latest_status(events):
    out = {}
    for oid, ts, s in events: out.setdefault(oid, s)
    return out
