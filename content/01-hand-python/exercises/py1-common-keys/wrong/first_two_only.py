def common_keys(dicts):
    if not dicts: return []
    keys = set(dicts[0])
    if len(dicts) > 1: keys &= set(dicts[1])
    return sorted(keys)
