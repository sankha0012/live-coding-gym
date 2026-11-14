import random


def sample_ids(ids, k, seed):
    return random.Random(seed).sample(list(ids), k)
