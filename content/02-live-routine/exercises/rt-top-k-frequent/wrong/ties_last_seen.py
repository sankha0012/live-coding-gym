def top_k(items, k):
    counts = {}
    last = {}
    for i, x in enumerate(items):
        counts[x] = counts.get(x, 0) + 1
        last[x] = i
    return sorted(counts, key=lambda x: (-counts[x], last[x]))[:k]
