def final_state(events):
    out = {}
    for e in events:
        out[e["entity"]] = e["state"]
    return out
