**Why this matters.** Leaderboards and reports are rarely sorted by one thing. We need high scores first, and among equal scores, names from A to Z: two directions at once.

**How we get there.**
1. Use `sorted(records, ...)` rather than `records.sort()`. It returns a new list and leaves the input alone.
2. Give it a `key` function. A key may return a tuple, and Python compares tuples position by position, so later parts only break ties.
3. Put the score first. We want high to low but sorting is ascending, so negate it: `-r["score"]`.
4. Put the name second, unchanged, so ties go from A to Z.
5. The whole thing is `sorted(records, key=lambda r: (-r["score"], r["name"]))`.

**Check it.** An empty list gives an empty list, and negative scores still work after negating. Sorting is `O(n log n)`.

**Watch out.** `reverse=True` reverses the whole order, so ties come out Z to A. Negating the score flips only the part we want.
