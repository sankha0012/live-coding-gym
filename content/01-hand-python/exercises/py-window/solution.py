def max_in_window(ts, w=60):
    ts = sorted(ts)
    best, left = 0, 0
    for right in range(len(ts)):
        while ts[right] - ts[left] >= w:
            left += 1
        best = max(best, right - left + 1)
    return best
