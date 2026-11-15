def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals, key=lambda x: x[1]):
        if merged and start <= merged[-1][1]:
            merged[-1][0] = min(merged[-1][0], start)
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
