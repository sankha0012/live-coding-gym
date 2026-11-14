from collections import Counter


def first_unique(s: str) -> int:
    counts = Counter(s)
    for i, ch in ____(s):
        if counts[ch] == ____:
            return i
    return ____
