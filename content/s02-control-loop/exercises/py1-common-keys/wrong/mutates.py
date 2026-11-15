def common_keys(dicts):
    if not dicts: return []
    first = dicts[0]
    for d in dicts[1:]:
        for k in list(first):
            if k not in d: del first[k]
    return sorted(first)
