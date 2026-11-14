def top_k(pairs, k):
    if k <= 0:
        return []
    pairs.sort(key=lambda p: -p[1])
    return pairs[:k]
