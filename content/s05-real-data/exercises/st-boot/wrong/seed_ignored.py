import random

def bootstrap_ci(xs, B=1000, seed=0):
    n = len(xs)
    means = sorted(sum(random.choices(xs, k=n)) / n for _ in range(B))
    return means[int(0.025 * B)], means[int(0.975 * B) - 1]
