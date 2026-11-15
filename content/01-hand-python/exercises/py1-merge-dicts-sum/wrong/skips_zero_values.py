def merge_dicts_sum(dicts: list) -> dict:
    out = {}
    for d in dicts:
        for k, v in d.items():
            if v:
                out[k] = out.get(k, 0) + v
    return out
