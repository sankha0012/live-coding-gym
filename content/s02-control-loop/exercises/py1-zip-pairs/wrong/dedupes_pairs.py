def pairs(items: list) -> list:
    return list(dict.fromkeys(zip(items, items[1:])))
