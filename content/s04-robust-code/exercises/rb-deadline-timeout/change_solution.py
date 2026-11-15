def process_until(items, handler, deadline, clock, max_items=None):
    items = list(items)
    results = []
    for i, item in enumerate(items):
        if (max_items is not None and i >= max_items) or clock() >= deadline:
            return results, items[i:]
        results.append(handler(item))
    return results, []
