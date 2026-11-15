def apply_n_times(f, n, x):
    if n == 0: return x
    for _ in range(n - 1 if n > 1 else 0):
        x = f(x)
    return x
