def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    merged = []
    for iv in sorted(intervals):
        if merged and iv[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], iv[1])
        else:
            merged.append(iv)
    return merged
