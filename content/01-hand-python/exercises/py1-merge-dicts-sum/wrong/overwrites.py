def merge_dicts_sum(dicts: list) -> dict:
    out = {}
    for d in dicts:
        out.update(d)
    return out
