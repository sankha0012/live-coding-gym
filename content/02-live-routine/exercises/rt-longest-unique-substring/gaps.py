def longest_unique(s: str) -> int:
    last = {}
    start = 0
    best = 0
    for i, ch in enumerate(____):
        if ch in last and last[ch] >= ____:
            start = last[ch] + ____
        last[ch] = i
        best = max(best, i - start + 1)
    return best
