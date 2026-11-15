def longest_unique(s):
    last = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = i
        last[ch] = i
        best = max(best, i - start + 1)
    return best
