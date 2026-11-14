from collections import Counter


def first_unique(s):
    counts = Counter(s)
    for ch in s:
        if counts[ch] == 1:
            return s.index(ch)
    return 0
