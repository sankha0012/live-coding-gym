def mean_std(xs):
    n = len(xs); m = sum(xs) / n
    return m, (sum((x - m) ** 2 for x in xs[1:]) / (n - 1)) ** 0.5
