def chunk(items, size):
    if not items: return []
    if size < 1: raise ValueError("size")
    return [items[i:i+size] for i in range(0, len(items), size)]
