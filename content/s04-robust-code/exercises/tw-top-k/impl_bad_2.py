def top_k(pairs, k):
    if k <= 0:
        return []
    return sorted(pairs, key=lambda p: -p[1])[:k + 1]
