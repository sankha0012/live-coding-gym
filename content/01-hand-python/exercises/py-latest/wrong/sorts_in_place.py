def latest_status(events):
    events.sort(key=lambda e: e[1])
    return {oid: s for oid, ts, s in events}
