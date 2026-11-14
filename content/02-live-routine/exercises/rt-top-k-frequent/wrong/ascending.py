from collections import Counter


def top_k(items: list, k: int) -> list:
    counts = Counter(items)
    return sorted(counts, key=lambda x: counts[x])[:k]
