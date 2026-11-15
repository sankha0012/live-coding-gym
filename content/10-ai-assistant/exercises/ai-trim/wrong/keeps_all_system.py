def trim_history(messages, budget):
    cost=lambda m: len(m[1].split())
    sysm=[m for m in messages if m[0]=="system"]
    used=sum(cost(m) for m in sysm); keep=set(map(id,sysm))
    for m in reversed(messages):
        if m[0]=="system": continue
        if used+cost(m)>budget: break
        keep.add(id(m)); used+=cost(m)
    return [m for m in messages if id(m) in keep]
