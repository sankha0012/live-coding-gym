def process_until(items, handler, deadline, clock):
    items = list(items)
    results = []
    for i, item in enumerate(items):
        if clock() >= deadline:
            return results, items[i:]
        r = handler(item)
        if r:
            results.append(r)
    return results, []
