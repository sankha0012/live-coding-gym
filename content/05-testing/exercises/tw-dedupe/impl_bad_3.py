def dedupe(items):
    seen = set()
    i = 0
    while i < len(items):
        if items[i] in seen:
            items.pop(i)
        else:
            seen.add(items[i])
            i += 1
    return items
