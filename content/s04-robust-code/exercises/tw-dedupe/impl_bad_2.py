def dedupe(items):
    seen = set()
    out = []
    for x in reversed(items):
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out[::-1]
