from collections import Counter


def top_k(items: list, k: int, min_count: int = 1) -> list:
    counts = Counter(items)  # keeps first-seen order
    ordered = sorted(counts, key=lambda x: -counts[x])  # sort is stable
    ordered = [x for x in ordered if counts[x] >= min_count]
    return ordered[:k]
