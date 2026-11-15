def max_in_window(ts, w=60):
    best, left = 0, 0
    for r in range(len(ts)):
        while ts[r] - ts[left] >= w: left += 1
        best = max(best, r - left + 1)
    return best
