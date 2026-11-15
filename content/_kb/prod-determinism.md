---
title: "Determinism: seeds, ordering, time"
summary: Same input gives the same output on every run and machine, by controlling randomness, order and the clock.
tags: [production, determinism]
---
```python
import random

def sample_ids(ids, k, seed):
    rng = random.Random(seed)           # own generator, not the global one
    return rng.sample(sorted(ids), k)   # sort first: set order is not stable

def top(scores, n):
    # ties broken by name, so the result never depends on input order
    return sorted(scores, key=lambda kv: (-kv[1], kv[0]))[:n]

def is_stale(saved_at, now, max_age):   # now is passed in, never read here
    return now - saved_at > max_age
```

- Use it for sampling, splits, rankings, reports and anything a test must reproduce.
- Key rule: every source of variation (seed, order, clock) is an input of the function.
- Say: "I inject the seed and the clock and I define the tie-break, so a rerun gives identical output."

<!-- more -->

## Details

There are three usual sources of non-determinism.

**Randomness.** Create `random.Random(seed)` and pass it around. The global `random.seed()` is shared with every library in the process.

**Ordering.** Sets have no defined order, and for strings it changes between processes. Sort before you sample, take the first item or write output. A sort key must be total: add a unique field as the last tie-break.

**Time.** A call to `time.time()` or `datetime.now()` inside the logic makes the result depend on when it ran. Take `now` or a `clock` function as a parameter.

```python
sample_ids({"d", "b", "a", "c"}, 2, seed=7)       # ['c', 'a']
sample_ids({"a", "b", "c", "d"}, 2, seed=7)       # ['c', 'a']  same set, same seed
top([("b", 2), ("a", 2), ("c", 5)], 2)            # [('c', 5), ('a', 2)]
is_stale(saved_at=100, now=161, max_age=60)       # True
```

For stable buckets across machines use `hashlib`, not the built-in `hash()`, which is salted per process for strings.

Float sums depend on the order of addition, so sort or use `math.fsum` when exact equality matters.

## Common mistakes

- Seeding the global generator and assuming no other code draws from it.
- Iterating over a set or over `dict` keys built from a set, then taking "the first".
- Sorting by score only, so ties come out in input order.
- Calling the real clock inside a function, which also makes it hard to test.
- Using `hash(user_id) % 100` for an assignment that must survive a restart.

## See also

- [Random numbers and seeds](#/kb/py-random-seeds)
- [Stable hashing with hashlib (and why not hash())](#/kb/py-hashlib)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
