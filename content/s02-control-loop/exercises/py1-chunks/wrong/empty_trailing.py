def chunks(items, n):
    if n <= 0: raise ValueError
    out = [items[i:i + n] for i in range(0, len(items), n)]
    if len(items) % n == 0 and items: out.append([])
    return out
