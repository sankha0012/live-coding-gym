def batch_split(items, n):
    n = max(n, 1)
    return [items[i:i + n] for i in range(0, len(items), n)]
