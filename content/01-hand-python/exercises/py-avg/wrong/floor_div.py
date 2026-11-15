from collections import defaultdict
def avg_by_customer(rows):
    t, n = defaultdict(int), defaultdict(int); seen=set()
    for c, v in rows:
        seen.add(c)
        if v is not None: t[c] += v; n[c] += 1
    return {c: (t[c] // n[c] if n[c] else None) for c in seen}
