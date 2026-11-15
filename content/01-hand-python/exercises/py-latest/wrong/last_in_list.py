def latest_status(events):
    return {oid: s for oid, ts, s in events}
