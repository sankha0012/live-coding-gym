import random


def sample_ids(ids, k, seed):
    return tuple(random.Random(seed).sample(list(ids), k))
