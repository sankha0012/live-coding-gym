def ks(y, s):
    goods = [si for yi, si in zip(y, s) if yi == 0]
    bads = [si for yi, si in zip(y, s) if yi == 1]
    best = 0.0
    for t in sorted(set(s)):
        cg = sum(g <= t for g in goods) / len(goods)
        cb = sum(b <= t for b in bads) / len(bads)
        best = max(best, cg - cb)
    return best
