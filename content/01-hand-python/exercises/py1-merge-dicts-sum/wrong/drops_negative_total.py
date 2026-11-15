def merge_dicts_sum(dicts: list) -> dict:
    out = {}
    for d in dicts:
        for k, v in d.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v > 0}
