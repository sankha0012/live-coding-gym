---
title: Canary, shadow and A/B assignment with stable hashing
summary: Send a fixed, repeatable share of users to a new model by hashing their id into a bucket.
tags: [production, deployment, hashing]
---
```python
import hashlib

def bucket(key, salt, buckets=100):
    digest = hashlib.sha256(f"{salt}:{key}".encode()).hexdigest()
    return int(digest, 16) % buckets    # same key and salt -> same bucket, on any machine

def variant(user_id, experiment, canary_pct):
    return "canary" if bucket(user_id, experiment) < canary_pct else "stable"
```

- Use it to roll out a model step by step or to split users for an experiment.
- Key rule: the assignment is a pure function of the id and a salt. No random call, no stored table.
- Say: "A user stays in the same group on every request and every server, and raising the percentage only adds users."

<!-- more -->

## Details

Three ways to try a new model on real traffic:

- **Canary.** A small share (1%, then 5%, 25%, 100%) gets the new model's answers. You watch errors and latency and roll back if they get worse.
- **Shadow.** The new model runs on the same requests, but its answer is only logged. Users always get the old answer. No user risk, but double compute.
- **A/B test.** A fixed split, held for a planned time, to measure a business metric with a statistical test.

```python
users = [f"user-{i}" for i in range(1000)]
at_10 = {u for u in users if variant(u, "ranker-v2", 10) == "canary"}
at_25 = {u for u in users if variant(u, "ranker-v2", 25) == "canary"}
len(at_10), len(at_25)       # (96, 255)   close to 10% and 25%, not exact
at_10 <= at_25               # True   ramping up keeps the earlier users
bucket("user-1", "ranker-v2") == bucket("user-1", "pricing-test")   # False  the salt separates experiments
```

A shadow call must never hurt the live path:

```python
def serve(x, live, shadow, log):
    result = live(x)
    try:
        log({"live": result, "shadow": shadow(x)})
    except Exception as e:
        log({"shadow_error": type(e).__name__})
    return result               # always the live answer
```

In a real service the shadow call also runs after the response or in the background, so it adds no latency.

## Common mistakes

- Using the built-in `hash()`: for strings it changes between processes.
- Using `random.random() < 0.1` per request, so one user flips between models.
- Using the same salt for every experiment, so the same users are always the test group.
- Comparing with `<=`, which gives 11 buckets out of 100 for "10 percent".
- Hashing an `int` id on one service and its string form on another. Convert with `str()` first.

## See also

- [Stable hashing with hashlib (and why not hash())](#/kb/py-hashlib)
- [A/B tests and the two-proportion z-test](#/kb/ml-ab-test-z)
- [Determinism: seeds, ordering, time](#/kb/prod-determinism)
