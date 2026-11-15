## Contract

`sample_ids(ids, k, seed) -> list`.

- `ids` is a list of any items (strings, dicts, lists). Items are picked by position, so a list holding equal values twice may return that value twice.
- Returns a new list with `k` items from `ids`, none taken from the same position twice. The items themselves are the same objects, not copies. The order is whatever the random draw gives, not the original order.
- The same `ids`, `k` and `seed` always give the same list, no matter what other code does with `random` in between.
- The global `random` generator is left exactly as it was: after the call it produces the same numbers as if `sample_ids` had never run.
- The `ids` list is not modified.
- `k == 0` returns `[]` (also for an empty `ids`). A negative `k`, or `k` above `len(ids)`, raises `ValueError`. `k == len(ids)` is allowed.
- Different seeds should give different samples; the result must not be a fixed slice.

## Library notes

- `random.Random(seed)` creates an independent generator object with its own state; `random.seed(seed)` instead resets the shared global one.
- `Random.sample(population, k)` returns a new list of `k` unique positions' items and raises `ValueError` if `k` is larger than the population. The population must be a sequence, not a set.
- `Random.shuffle(x)` shuffles a list in place and returns `None`.
- `random.getstate()` returns the generator state, which lets you check that something left it untouched.

## Gotchas

- Seeding the global generator makes code that is far away change behavior.
- A reproducible audit needs a stable input order; sampling from a set or unsorted query result changes between runs.
- Do not shuffle the caller's list in place.
