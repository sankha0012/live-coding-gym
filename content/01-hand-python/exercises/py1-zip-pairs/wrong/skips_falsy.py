def pairs(items: list) -> list:
    return [(a, b) for a, b in zip(items, items[1:]) if a and b]
