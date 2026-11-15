def common_keys(dicts: list) -> list:
    keys = set()
    for d in dicts:
        keys |= set(d)
    return sorted(keys)
