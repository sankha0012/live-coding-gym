def top_k(items, k):
    ordered = sorted(items, key=lambda x: -items.count(x))
    return ordered[:k]
