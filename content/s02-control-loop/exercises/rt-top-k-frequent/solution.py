from collections import Counter


def top_k(items: list, k: int) -> list:
    counts = Counter(items)  # keeps first-seen order
    ordered = sorted(counts, key=lambda x: -counts[x])  # sort is stable
    return ordered[:k]
