def merge_shifts(shifts):
    merged = []
    for sh in sorted(shifts):
        if merged and sh[0] <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], sh[1])
        else: merged.append(sh)
    return merged
