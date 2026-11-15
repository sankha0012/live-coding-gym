def final_state(events):
    seen = set()
    best = {}
    for e in events:
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        cur = best.get(e["entity"])
        if cur is None or e["ts"] >= cur["ts"]:
            best[e["entity"]] = e
    return {entity: e["state"] for entity, e in best.items() if e["state"] != "deleted"}
