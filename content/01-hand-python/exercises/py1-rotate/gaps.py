def rotate(items: list, k: int) -> list:
    if not items:
        return []
    k ____ len(items)
    return items[-k:] + items[:-k]
