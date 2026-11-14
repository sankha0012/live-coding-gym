import random


def sample_ids(ids, k, seed):
    random.seed(seed)
    return random.sample(list(ids), k)
