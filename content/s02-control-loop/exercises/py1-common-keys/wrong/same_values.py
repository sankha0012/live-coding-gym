def common_keys(dicts):
    if not dicts: return []
    items = set(dicts[0].items())
    for d in dicts[1:]: items &= set(d.items())
    return sorted(k for k, v in items)
