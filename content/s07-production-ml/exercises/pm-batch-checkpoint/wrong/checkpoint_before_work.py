def run_batch(items, handler, store):
    results = store.setdefault("results", [])
    store.setdefault("next", 0)
    while store["next"] < len(items):
        item = items[store["next"]]
        store["next"] += 1
        results.append(handler(item))
    return results
