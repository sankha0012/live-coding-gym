def mean_std(xs):
    n = len(xs); s = sorted(xs); m = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    return m, (sum((x - m) ** 2 for x in xs) / (n - 1)) ** 0.5
