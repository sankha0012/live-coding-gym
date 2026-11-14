def invert_dict(d: dict) -> dict:
    out = {}
    for key, value in d.items():
        out.setdefault(value, []).append(key)
    return {value: sorted(keys) for value, keys in out.items()}
