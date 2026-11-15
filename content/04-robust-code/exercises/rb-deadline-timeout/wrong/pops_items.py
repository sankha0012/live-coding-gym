def process_until(items, handler, deadline, clock):
    results = []
    while items:
        if clock() >= deadline:
            return results, items
        results.append(handler(items.pop(0)))
    return results, []
