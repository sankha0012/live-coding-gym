def chunks(items, n):
    if n <= 0: raise ValueError
    out = [items[i:i + n] for i in range(0, len(items), n)]
    if len(out) > 1 and len(out[-1]) < n:
        out[-2] += out.pop()
    return out
