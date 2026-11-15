def merge_shifts(shifts):
    merged = []; prev_end = None
    for s, e in sorted(shifts):
        if merged and s <= prev_end: merged[-1][1] = max(merged[-1][1], e)
        else: merged.append([s, e])
        prev_end = e
    return merged
