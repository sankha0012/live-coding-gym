def ks(y, s):
    goods = [si for yi, si in zip(y, s) if yi == 0]
    bads = [si for yi, si in zip(y, s) if yi == 1]
    best = 0.0
    for t in sorted(set(s)):
        cg = sum(g <= t for g in goods) / (len(y) / 2)
        cb = sum(b <= t for b in bads) / (len(y) / 2)
        best = max(best, abs(cg - cb))
    return best
