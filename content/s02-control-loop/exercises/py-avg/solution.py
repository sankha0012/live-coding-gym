from collections import defaultdict

def avg_by_customer(rows):
    total, count = defaultdict(float), defaultdict(int)
    seen = set()
    for cid, v in rows:
        seen.add(cid)
        if v is not None:
            total[cid] += v
            count[cid] += 1
    return {cid: (total[cid] / count[cid] if count[cid] else None) for cid in seen}
