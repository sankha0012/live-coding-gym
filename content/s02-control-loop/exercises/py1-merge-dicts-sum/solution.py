def merge_dicts_sum(dicts: list) -> dict:
    out = {}
    for d in dicts:
        for key, value in d.items():
            out[key] = out.get(key, 0) + value
    return out
