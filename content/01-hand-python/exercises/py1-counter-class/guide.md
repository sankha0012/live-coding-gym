**Why this matters.** A counter is a dict with a few useful operations on top. The class lessons are where state lives, and how to make a sorted result fully deterministic.

**How we get there.**
1. In `__init__`, create `self._counts = {}`. Making it here gives each instance its own dict, not one shared by all.
2. `add` updates with `self._counts.get(item, 0) + k`. The default of 0 handles an item we have never seen.
3. `count` reads with the same `.get(item, 0)`, so a missing item is 0. `total` is `sum(self._counts.values())`.
4. `most_common` sorts the items with `key=lambda kv: (-kv[1], kv[0])`: biggest count first, then the item for ties. Then it slices `[:n]`.

**Check it.** An empty counter returns `[]`, a large `n` returns everything and `n = 0` returns `[]`. Sorting m distinct items costs O(m log m).

**Watch out.** A dict defined on the class is shared by every instance, and sorting by count alone leaves ties in insertion order.
