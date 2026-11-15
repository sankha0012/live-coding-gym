import random


def sample_ids(ids, k, seed):
    pool = sorted(set(ids))
    return random.Random(seed).sample(pool, k)
