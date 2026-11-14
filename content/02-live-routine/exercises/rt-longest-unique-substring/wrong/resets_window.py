def longest_unique(s: str) -> int:
    seen = set()
    best = 0
    for ch in s:
        if ch in seen:
            seen = set()
        seen.add(ch)
        best = max(best, len(seen))
    return best
