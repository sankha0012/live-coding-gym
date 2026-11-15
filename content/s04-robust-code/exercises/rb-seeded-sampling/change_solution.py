import random


def sample_ids(ids, k, seed, exclude=()):
    pool = [x for x in ids if x not in exclude]
    return random.Random(seed).sample(pool, k)
