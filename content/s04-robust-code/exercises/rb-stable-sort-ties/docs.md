## Contract

`rank(records) -> list`.

Each record is a dict with `"id"` (a string) and `"score"` (a number or `None`); it may also hold other keys. The result is a new list, and neither the input list nor its dicts are changed. An empty list returns `[]`. All records are kept, including repeated ids.

Order, from first to last:

1. Higher score first. Scores may be ints or floats, negative or zero, and are compared as given, without rounding. Mixed values such as `2` and `2.0` are equal.
2. A score of `None` is missing, not zero; those records go after every record with a number.
3. Equal scores are ordered by `id`, ascending alphabetical.
4. If score and id are both equal, the original input order is kept. This applies to `None` scores too.

Example: scores `[2, None, 5, 2]` with ids `b, a, c, a` give `c`, `a` (2), `b` (2), `a` (None).

## Library notes

- `sorted(iterable, key=f, reverse=False)` returns a new list; `list.sort()` sorts in place and returns `None`. Both are stable: equal keys keep input order.
- Key tuples compare element by element, so `(1, "b") < (2, "a")`. Comparing `None` with a number raises `TypeError`.
- `reverse=True` keeps equal items in their original order, it does not flip them.
- Negating a number (`-x`) flips its order inside a key, but does not work for strings.

## Gotchas

- Sorting in place changes the caller's list, which breaks reproducible runs.
- Without an explicit tie-break, order can change between runs if the input arrives in a different order.
- A `None` in a sort key crashes in production the first day a score is missing.
