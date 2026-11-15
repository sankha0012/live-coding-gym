def pairs(items: list) -> list:
    return [[items[i], items[i + 1]] for i in range(len(items) - 1)]
