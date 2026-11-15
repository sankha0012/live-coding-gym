def process_until(items, handler, deadline, clock):
    items = list(items)
    results = []
    for i, item in enumerate(items):
        results.append(handler(item))
        if clock() >= deadline:
            return results, items[i + 1:]
    return results, []
