from collections import Counter

def top_k_dishes(orders, k):
    counts = Counter()
    for items in orders:
        counts.update(items)
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [dish for dish, _ in ranked[:k]]
