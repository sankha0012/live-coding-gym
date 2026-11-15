A ranking job must give the same order on every run. Write `rank(records)`. Each record is a dict with `"id"` (a string) and `"score"` (a number or `None`).

- Return a new list. Do not change the input list or its dicts.
- Higher score first.
- Records with `score` `None` go last.
- Equal scores are ordered by `id`, alphabetical (ascending).
- If both `score` and `id` are equal, keep the original input order.
- An empty list returns an empty list.

Example: scores `[2, None, 5, 2]` with ids `b, a, c, a` give the order `c`, then `a` (2), then `b` (2), then `a` (None).

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
