import random


def sample_ids(ids, k, seed):
    return random.Random().sample(list(ids), k)
