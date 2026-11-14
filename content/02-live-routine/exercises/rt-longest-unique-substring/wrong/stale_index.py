def longest_unique(s: str) -> int:
    last = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best
