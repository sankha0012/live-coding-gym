# Determinism

## The problem it solves

A deterministic function gives the same output for the same input, every run, on every machine. Production ML code needs this. If a train/test split changes between runs, you cannot compare two models. If a report changes when nobody changed the data, nobody trusts it. In an interview, a test that passes today and fails tomorrow is a failed test.

Non-determinism hides in a few places: random numbers, ordering, per-process hashing and time.

## The smallest runnable example

```python
import hashlib
import random


def sample_ids(ids, k, seed):
    rng = random.Random(seed)          # own generator, not the global one
    return rng.sample(sorted(ids), k)  # sort first: a set has no fixed order


def bucket(user_id: str, n: int = 10) -> int:
    digest = hashlib.md5(user_id.encode()).hexdigest()
    return int(digest, 16) % n


ids = {"u3", "u1", "u2", "u9", "u7"}
assert sample_ids(ids, 2, seed=42) == sample_ids(ids, 2, seed=42)
assert bucket("user-123") == bucket("user-123")
print(sample_ids(ids, 2, seed=42), bucket("user-123"))
```

Three habits are in this code. The generator is created from a seed and passed around. The input is sorted before sampling. The bucket uses hashlib, not `hash()`.

## Where non-determinism hides

**Seeds.** `random.random()` uses a global generator. Any other code can move its state. Create `random.Random(seed)` inside your function and use it. The same idea applies to numpy: use `numpy.random.default_rng(seed)`.

**Ordering.** Dicts keep insertion order since Python 3.7, so a dict built from the same input in the same order is stable. Sets are not. The order of a set of strings can change from one run to the next. Never loop over a set and let the order change the result. Use `sorted(the_set)`.

**Sorting.** `sorted` is stable: items with equal keys keep their input order. That is only deterministic if the input order is deterministic. When two rows tie, add a tie-break to the key so the result does not depend on how the data arrived: `sorted(rows, key=lambda r: (-r["score"], r["id"]))`.

**hash().** The built-in `hash()` of a string is randomised per process on purpose (to stop hash-flooding attacks). Run Python twice and you get two different values. Never use it to assign users to folds, buckets or experiment groups. Use `hashlib` (md5 or sha256 on encoded bytes) instead. Integers hash to themselves, which is why this trap hides in tests that use numbers.

**Time.** `datetime.now()` is different every call. Pass the time in as a parameter or inject a clock (see the lesson on injecting clocks). Also be careful with time zones. A naive datetime has no zone, and comparing it to an aware one raises an error. Store and compare in UTC: `datetime.now(timezone.utc)`. Convert to local time only when you display it.

## Three traps people hit

1. **Seeding the global generator and thinking you are done.** `random.seed(0)` works until another library or another test calls the global generator in between. Use a local `random.Random(seed)`.
2. **Trusting set or dict order from outside.** A dict built from a database query or a set of ids can come in a different order next run. Sort before you depend on the order, and sort with a full key.
3. **Using hash() for anything that must be stable.** It passes every test in one process and breaks when the job restarts. Use hashlib.

A fourth trap is close behind: floating point sums depend on order. Summing the same numbers in a different order can change the last digits. Sort the input or use `math.fsum` when you compare totals exactly.

## How to prove it

Write the test that runs the function twice, and for hashes, compare against a fixed expected value. For example, `bucket("user-123")` always returns the same number, so you can hard-code it in a test. A test that also runs the code in a fresh process (`subprocess`) catches `hash()` mistakes, but for a short interview the "call twice and compare" check with sorted input is enough.

## Say it like this

"I make the function deterministic on purpose. Randomness comes from a local generator created from a seed that the caller passes in. I sort anything that came from a set, and I break ties with an id so the order does not depend on arrival. For bucketing I use hashlib because the built-in hash of a string changes per process. Time comes in as a parameter, and I keep everything in UTC. That way the same input gives the same output, and my tests can check it."
