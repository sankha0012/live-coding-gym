def final_state(events):
    seen, ts_of, out = set(), {}, {}
    for e in events:
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        if e["ts"] >= ts_of.get(e["entity"], 0):
            ts_of[e["entity"]] = e["ts"]
            out[e["entity"]] = e["state"]
    return out
