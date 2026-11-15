from collections import defaultdict
def avg_by_customer(rows):
    t, n = defaultdict(float), defaultdict(int)
    for c, v in rows:
        if v is not None:
            t[c] += v; n[c] += 1
        else:
            t[c] += 0; n[c] += 0
    return {c: (t[c] / n[c] if n[c] else 0) for c in t}
