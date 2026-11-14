def latest_status(events):
    best = {}
    for oid, ts, status in events:
        if oid not in best or ts > best[oid][0]:
            best[oid] = (ts, status)
    return {oid: s for oid, (ts, s) in best.items()}
