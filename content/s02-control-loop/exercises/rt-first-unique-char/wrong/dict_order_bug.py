def first_unique(s):
    seen = set()
    for i, ch in enumerate(s):
        if ch not in seen and s.count(ch) == 1:
            return i
        seen.add(ch)
    return len(s) - 1 if s else -1
