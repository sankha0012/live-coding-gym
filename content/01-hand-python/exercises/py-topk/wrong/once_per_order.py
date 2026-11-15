from collections import Counter
def top_k_dishes(orders, k):
    c = Counter()
    for o in orders: c.update(set(o))
    return [d for d, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]
