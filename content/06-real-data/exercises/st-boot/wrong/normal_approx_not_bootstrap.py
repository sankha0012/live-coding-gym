import random

def bootstrap_ci(xs, B=1000, seed=0):
    n = len(xs); m = sum(xs) / n
    sd = (sum((x - m) ** 2 for x in xs) / (n - 1)) ** 0.5
    return m - 1.96 * sd / n ** 0.5, m + 1.96 * sd / n ** 0.5
