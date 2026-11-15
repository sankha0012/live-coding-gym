def final_state(events):
    best = {}
    for e in events:
        cur = best.get(e["entity"])
        if cur is None or e["ts"] >= cur["ts"]:
            best[e["entity"]] = e
    return {entity: e["state"] for entity, e in best.items()}
