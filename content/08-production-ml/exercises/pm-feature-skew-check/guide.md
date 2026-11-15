**Why this matters.** A model trained on offline features can be quietly wrong if the online pipeline computes them differently. Comparing the two feature dicts for the same entity finds this before users do.

**How we get there.**
1. Loop over `sorted(set(online) | set(offline))`, so a feature missing on either side is visited, and the output order is stable.
2. If the name is not in `online`, report `"missing_online"`. If it is not in `offline`, report `"missing_offline"`.
3. For features in both, handle nulls first. A null is `None` or a float that is not equal to itself, because `nan != nan`. Both null is fine, and one null is a `"diff"`.
4. For two numbers, excluding `bool`, flag a `"diff"` only when `abs(a - b) > tolerance`. Exactly at the tolerance is fine, and `3` equals `3.0`.
5. Anything else, like strings and bools, is a `"diff"` when `a != b`.

**Check it.** `0` and `""` are real values, not nulls, which is why we test for `None` explicitly. Time is O(n log n) from the sort.

**Watch out.** Comparing floats with `==` flags harmless rounding noise, and comparing `nan == nan` reports skew that is not there.
