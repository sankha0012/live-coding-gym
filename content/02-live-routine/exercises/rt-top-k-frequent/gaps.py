from collections import Counter


def top_k(items: list, k: int) -> list:
    counts = ____(items)
    ordered = sorted(counts, key=lambda x: -counts[x])
    return ordered[:____]
