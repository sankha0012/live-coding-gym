import random

def bootstrap_ci(xs, B=1000, seed=0):
    random.seed(seed)
    n = len(xs)
    means = sorted(sum(random.sample(xs, n)) / n for _ in range(B))
    return means[int(0.025 * B)], means[int(0.975 * B) - 1]
