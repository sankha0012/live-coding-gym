def common_keys(dicts: list) -> list:
    if not dicts:
        return []
    keys = set(dicts[0])
    for d in dicts[1:]:
        keys &= set(d)
    return sorted(keys)
