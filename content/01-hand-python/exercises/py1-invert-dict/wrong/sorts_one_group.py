def invert_dict(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        out.setdefault(v, []).append(k)
    first = next(iter(out), None)
    if first is not None:
        out[first].sort()
    return out
