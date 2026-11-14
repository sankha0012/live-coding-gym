from collections import Counter


def first_unique(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] != 1:
            break
        return i
    return -1
