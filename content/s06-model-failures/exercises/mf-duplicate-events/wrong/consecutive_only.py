def dedupe_events(events):
    u=[]
    for e in events:
        if u and u[-1]["id"]==e["id"]: continue
        u.append(e)
    return u, len(events)-len(u)
