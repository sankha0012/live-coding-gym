def chunk(items, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    out = []
    for i in range(0, len(items) + 1, size):
        out.append(items[i:i + size])
    return out
