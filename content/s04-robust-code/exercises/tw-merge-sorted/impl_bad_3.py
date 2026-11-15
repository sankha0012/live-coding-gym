def merge_sorted(a, b):
    out = []
    while a and b:
        if a[0][0] <= b[0][0]:
            out.append(a.pop(0))
        else:
            out.append(b.pop(0))
    return out + a + b
