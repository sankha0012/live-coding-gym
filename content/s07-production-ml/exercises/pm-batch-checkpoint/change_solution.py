def run_batch(items: list, handler, store: dict, limit=None) -> list:
    results = store.setdefault("results", [])
    store.setdefault("next", 0)
    done = 0
    while store["next"] < len(items) and (limit is None or done < limit):
        result = handler(items[store["next"]])
        results.append(result)
        store["next"] += 1
        done += 1
    return results
