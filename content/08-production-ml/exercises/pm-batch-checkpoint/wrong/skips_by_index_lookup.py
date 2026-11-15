def run_batch(items, handler, store):
    results = store.setdefault("results", [])
    store.setdefault("next", 0)
    for item in items:
        if items.index(item) < store["next"]:
            continue
        results.append(handler(item))
        store["next"] += 1
    return results
