def longest_unique(s):
    seen = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= start:
            best = max(best, i - start)
            start = seen[ch] + 1
        seen[ch] = i
    return best
