from collections import Counter

def top_k(items, k):
    items.sort()
    counts = Counter(items)
    return sorted(counts, key=lambda x: -counts[x])[:k]
