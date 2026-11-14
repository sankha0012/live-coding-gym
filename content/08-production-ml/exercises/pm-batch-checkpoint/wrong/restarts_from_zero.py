def run_batch(items, handler, store):
    results = []
    for item in items:
        results.append(handler(item))
        store["next"] = len(results)
        store["results"] = results
    return results
