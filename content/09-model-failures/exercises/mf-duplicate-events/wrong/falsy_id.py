def dedupe_events(events):
    seen=set(); u=[]
    for e in events:
        if e["id"] and e["id"] in seen: continue
        seen.add(e["id"]); u.append(e)
    return u, len(events)-len(u)
