import random

def bootstrap_ci(xs, B=1000, seed=0):
    random.seed(seed)
    n = len(xs); k = max(1, n // 2)
    means = sorted(sum(random.choices(xs, k=k)) / k for _ in range(B))
    return means[int(0.025 * B)], means[int(0.975 * B) - 1]
