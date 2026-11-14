def top_k(items: list, k: int) -> list:
    counts = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return sorted(counts, key=lambda x: (-counts[x], x))[:k]
