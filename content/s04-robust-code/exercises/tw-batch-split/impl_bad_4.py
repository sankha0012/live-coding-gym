def batch_split(items, n):
    if n == 0:
        raise ValueError("n must be at least 1")
    return [items[i:i + n] for i in range(0, len(items), n)]
