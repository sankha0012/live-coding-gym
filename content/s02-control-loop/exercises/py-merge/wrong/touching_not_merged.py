def merge_shifts(shifts):
    merged = []
    for s, e in sorted(shifts):
        if merged and s < merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
        else: merged.append([s, e])
    return merged
