def run_batch(items, handler, store):
    results = store.setdefault("results", [])
    store.setdefault("next", 0)
    while store["next"] < len(items):
        try:
            result = handler(items[store["next"]])
        except Exception:
            return results
        results.append(result)
        store["next"] += 1
    return results
