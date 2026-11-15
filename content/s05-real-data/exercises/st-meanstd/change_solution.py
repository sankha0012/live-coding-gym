def mean_std(xs, ddof=1):
    n = len(xs)
    m = sum(xs) / n
    var = sum((x - m) ** 2 for x in xs) / (n - ddof)
    return m, var ** 0.5
