def apply_n_times(f, n, x):
    for _ in range(n):
        x = f(x)
    return x
