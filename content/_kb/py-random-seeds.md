---
title: Random numbers and seeds
summary: Generate random numbers, choices and shuffles, and make them repeatable with a seeded Random object.
tags: [python, random, determinism]
---
```python
import random
rng = random.Random(42)           # your own generator with a fixed seed
rng.random()                      # 0.6394267984578837   float in [0, 1)
rng.randint(1, 6)                 # 1        both ends included
rng.choice(["a", "b", "c"])       # 'c'
rng.sample(range(10), 3)          # [4, 3, 8]   3 different items, new list
xs = [1, 2, 3, 4, 5]
rng.shuffle(xs)                   # returns None, xs is now [5, 4, 3, 1, 2]
```

- Same seed and same sequence of calls gives the same numbers every run.
- `random.Random(seed)` is a private generator. `random.seed(seed)` resets the shared global one.
- `shuffle` changes the list in place and returns `None`.

<!-- more -->

## Details

The module is pseudo-random: the numbers come from a formula that starts at the seed. With no seed, Python picks one from the operating system, so each run differs.

Prefer a private `Random` object and pass it in as a parameter. Then no other code can disturb your sequence, and a test can give a fixed seed:

```python
def roll_dice(n, rng=None):
    rng = rng or random.Random()
    return [rng.randint(1, 6) for _ in range(n)]

roll_dice(5, random.Random(7))    # [3, 2, 4, 6, 1]
roll_dice(5, random.Random(7))    # [3, 2, 4, 6, 1]   same seed, same result
```

More functions, all available on the module and on a `Random` object:

- `randrange(10)` is an integer from 0 to 9. The stop is excluded, like `range`.
- `uniform(1, 2)` is a float between 1 and 2.
- `choices(items, weights=[9, 1], k=5)` picks 5 items with replacement, so repeats are possible.
- `sample(items, k)` picks without replacement. It needs a sequence, not a set.
- `gauss(0, 1)` is a normal value with mean 0 and standard deviation 1.

To shuffle without changing the original, use `rng.sample(xs, k=len(xs))`.

NumPy has its own generator and its own seed: `np.random.default_rng(42)`. Seeding `random` does not seed NumPy.

## Common mistakes

- Writing `xs = random.shuffle(xs)`. Now `xs` is `None`.
- Forgetting that `randint(1, 6)` includes 6 but `randrange(1, 6)` does not.
- Seeding once and then adding a new random call earlier in the code. Every later value changes.
- Calling `random.choice([])`. It raises `IndexError`.
- Using `random` for passwords or tokens. Use the `secrets` module for security.

## See also

- [Determinism: seeds, ordering, time](#/kb/prod-determinism)
- [Stable hashing with hashlib (and why not hash())](#/kb/py-hashlib)
- [The bootstrap](#/kb/ml-bootstrap)
- Official docs: https://docs.python.org/3/library/random.html
