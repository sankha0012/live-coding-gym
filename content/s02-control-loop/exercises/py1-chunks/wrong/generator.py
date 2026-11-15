def chunks(items, n):
    if n <= 0: raise ValueError
    return (items[i:i + n] for i in range(0, len(items), n))
