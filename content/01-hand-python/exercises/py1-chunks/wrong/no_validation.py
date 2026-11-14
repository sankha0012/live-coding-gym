def chunks(items: list, n: int) -> list:
    return [items[i:i + n] for i in range(0, len(items), max(n, 1))]
