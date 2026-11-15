from collections import Counter

def first_unique(s):
    counts = Counter(s.lower())
    for i, ch in enumerate(s):
        if counts[ch.lower()] == 1:
            return i
    return -1
