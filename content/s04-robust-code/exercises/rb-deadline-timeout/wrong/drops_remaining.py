def process_until(items, handler, deadline, clock):
    results = []
    for item in items:
        if clock() >= deadline:
            break
        results.append(handler(item))
    return results, []
