def rotate(items: list, k: int) -> list:
    if not items:
        return []
    k %= len(items)
    if k == 0:
        return items
    return items[-k:] + items[:-k]
