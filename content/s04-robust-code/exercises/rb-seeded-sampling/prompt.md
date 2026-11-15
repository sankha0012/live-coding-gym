Write `sample_ids(ids, k, seed)` that picks `k` different ids at random for an audit, in a way that can be repeated exactly.

- Return a list of `k` items from `ids`, no item picked twice (by position).
- The same `ids`, `k` and `seed` always give the same list, even if other code calls `random` in between.
- Your function must not change the global `random` state: after the call, the global generator continues exactly as if it had not been called.
- Do not change the `ids` list.
- `k == 0` returns `[]`. If `k` is negative or larger than `len(ids)`, raise `ValueError`.
