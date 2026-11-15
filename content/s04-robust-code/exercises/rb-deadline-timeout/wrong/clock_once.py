def process_until(items, handler, deadline, clock):
    items = list(items)
    now = clock()
    results = []
    for i, item in enumerate(items):
        if now >= deadline:
            return results, items[i:]
        results.append(handler(item))
    return results, []
