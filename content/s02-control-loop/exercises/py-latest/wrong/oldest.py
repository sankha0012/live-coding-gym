def latest_status(events):
    best = {}
    for oid, ts, s in events:
        if oid not in best or ts < best[oid][0]: best[oid] = (ts, s)
    return {o: v[1] for o, v in best.items()}
