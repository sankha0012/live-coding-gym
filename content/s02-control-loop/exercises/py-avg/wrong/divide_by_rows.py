from collections import defaultdict
def avg_by_customer(rows):
    t, n = defaultdict(float), defaultdict(int)
    for c, v in rows:
        n[c] += 1
        if v is not None: t[c] += v
    return {c: (t[c] / n[c] if t[c] else None) for c in n}
