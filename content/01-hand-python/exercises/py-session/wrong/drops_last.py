def sessionize(timestamps, gap=30):
    ts = sorted(timestamps); s = []; cur = []
    for t in ts:
        if cur and t - cur[-1] > gap: s.append(cur); cur = []
        cur.append(t)
    return s
