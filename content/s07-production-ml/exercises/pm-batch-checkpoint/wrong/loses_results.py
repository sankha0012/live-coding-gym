def run_batch(items, handler, store):
    store.setdefault("next", 0)
    results = []
    while store["next"] < len(items):
        results.append(handler(items[store["next"]]))
        store["next"] += 1
    return results
