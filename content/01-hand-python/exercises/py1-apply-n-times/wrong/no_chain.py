def apply_n_times(f, n, x):
    r = x
    for _ in range(n):
        r = f(x)
    return r
