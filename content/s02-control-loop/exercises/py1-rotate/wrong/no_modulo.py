def rotate(items: list, k: int) -> list:
    return items[-k:] + items[:-k]
