def run_batch(items: list, handler, store: dict) -> list:
    results = store.setdefault("results", [])
    store.setdefault("next", 0)
    while store["next"] < len(items):
        result = handler(items[store["next"]])
        results.append(result)
        store["next"] += 1
    return results
