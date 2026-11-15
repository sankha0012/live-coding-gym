# Seeds and seeded sampling

## What it is

A seed fixes the starting state of a pseudo-random generator, so the same seed produces the same sequence of numbers. Seeded sampling means every random choice in your code, such as a train/test split, a subsample or a shuffle, comes from a generator whose seed you control. The result is reproducible: run it tomorrow, on another machine, and you get the same rows. See [Random seeds](#/kb/py-random-seeds) and [Determinism](#/kb/prod-determinism).

## How it breaks in production

The usual failure is the global generator. `random.seed(0)` at the top of a script seems enough, but any library, thread or earlier test that calls `random.random()` moves the shared state, so your sample changes for no visible reason. Another failure is sampling from a set: since Python 3.11 `random.sample` refuses sets, and iterating a set of strings gives a different order in each process because string hashing is randomised. A third is calling `hash(user_id) % 10` to pick a bucket: the value changes every time the process restarts, so a user lands in a different experiment group after each deploy. The symptom is always the same: two runs on identical data give different metrics, and nobody can tell whether the model or the sampling changed.

## The defence in code

```python
import hashlib
import random

import numpy as np


def sample_ids(ids, k, seed):
    rng = random.Random(seed)          # own generator, not the global one
    return rng.sample(sorted(ids), k)  # sorted: a set has no stable order


def bucket(user_id, n=10):
    digest = hashlib.md5(user_id.encode()).hexdigest()  # stable across processes
    return int(digest, 16) % n


ids = {"u3", "u1", "u2", "u9", "u7"}
assert sample_ids(ids, 2, seed=42) == sample_ids(ids, 2, seed=42)
assert bucket("user-123") == bucket("user-123")

a = np.random.default_rng(7).permutation(10)
b = np.random.default_rng(7).permutation(10)
assert (a == b).all()
print(sample_ids(ids, 2, seed=42), bucket("user-123"), a[:3])
```

The generator is created inside the function from a seed the caller passes in. The input is sorted before sampling. The bucket comes from `hashlib`, which gives the same digest in every process. In scikit-learn the same rule means passing `random_state=` to `train_test_split` and to every estimator that uses randomness.

## What to say in the interview

"Every random choice in my code comes from a local generator built from a seed that the caller passes in, so I never depend on the global state. I sort anything that came from a set before sampling it. For splits and experiment buckets I use hashlib, not the built-in hash, because that one changes per process. Then my test can run the function twice and assert equal results, and a metric change means the data or the model changed, not the dice."
