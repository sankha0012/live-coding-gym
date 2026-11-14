def merge_sorted(a, b):
    return sorted(a + b, key=lambda p: (p[0], p[1]))
