def longest_unique(s):
    seen = set()
    for ch in s:
        if ch in seen:
            break
        seen.add(ch)
    return len(seen)
