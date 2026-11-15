def avg_by_customer(rows):
    t, n = {}, {}
    for c, v in rows:
        if v is None: continue
        t[c] = t.get(c, 0) + v; n[c] = n.get(c, 0) + 1
    return {c: t[c] / n[c] for c in t}
