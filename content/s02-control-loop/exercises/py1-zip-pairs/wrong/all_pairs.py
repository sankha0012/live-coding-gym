def pairs(items: list) -> list:
    return [(a, b) for a in items for b in items if a != b]
