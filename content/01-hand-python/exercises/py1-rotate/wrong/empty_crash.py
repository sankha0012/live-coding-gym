def rotate(items: list, k: int) -> list:
    k %= len(items)
    return items[-k:] + items[:-k]
