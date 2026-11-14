def common_keys(dicts: list) -> list:
    if not ____:
        return []
    keys = set(dicts[0])
    for d in dicts[1:]:
        keys ____ set(d)
    return ____(keys)
