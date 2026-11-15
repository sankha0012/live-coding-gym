def mean_std(xs):
    n = len(xs); m = sum(xs) / n
    return round(m, 2), round((sum((x - m) ** 2 for x in xs) / (n - 1)) ** 0.5, 2)
