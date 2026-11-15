def apply_n_times(f, n, x):
    for _ in range(n + 1):
        x = f(x)
    return x
