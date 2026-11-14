def apply_n_times(f, n, x):
    for _ in range(1, n):
        x = f(x)
    return x
