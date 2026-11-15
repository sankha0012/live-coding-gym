from collections import Counter

def first_unique(s):
    counts = Counter(s)
    for i in range(len(s) - 1, -1, -1):
        if counts[s[i]] == 1:
            return i
    return -1
