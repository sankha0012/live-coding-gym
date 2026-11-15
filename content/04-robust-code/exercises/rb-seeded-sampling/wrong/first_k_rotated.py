import random


def sample_ids(ids, k, seed):
    if k < 0 or k > len(ids):
        raise ValueError("bad k")
    start = random.Random(seed).randrange(len(ids)) if ids else 0
    rot = list(ids[start:]) + list(ids[:start])
    return rot[:k]
