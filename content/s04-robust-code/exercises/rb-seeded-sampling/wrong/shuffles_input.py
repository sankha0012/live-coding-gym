import random


def sample_ids(ids, k, seed):
    if k < 0 or k > len(ids):
        raise ValueError("bad k")
    rng = random.Random(seed)
    rng.shuffle(ids)
    return ids[:k]
