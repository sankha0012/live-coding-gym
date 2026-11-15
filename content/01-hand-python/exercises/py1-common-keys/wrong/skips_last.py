def common_keys(dicts):
    if not dicts: return []
    keys = set(dicts[0])
    for d in dicts[1:-1]: keys &= set(d)
    return sorted(keys)
