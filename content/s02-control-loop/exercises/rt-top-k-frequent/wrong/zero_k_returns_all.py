from collections import Counter


def top_k(items, k):
    counts = Counter(items)
    ordered = sorted(counts, key=lambda x: -counts[x])
    return ordered[:k] if k else ordered
