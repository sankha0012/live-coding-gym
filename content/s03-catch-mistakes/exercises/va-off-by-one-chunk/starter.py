def chunk(items, size):
    """Split items into consecutive lists of at most `size` items.

    chunk([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
    Empty input returns []. size < 1 raises ValueError.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    out = []
    for i in range(0, len(items) - size, size):
        out.append(items[i:i + size])
    return out
