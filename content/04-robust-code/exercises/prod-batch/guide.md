**Why this matters.** In batch scoring, one bad row, say a missing feature, must not kill a job covering a million rows. The sneaky part is that a model can also "succeed" and return NaN, which is worse than an error because it flows downstream silently.

**How we get there.**
1. Loop over rows one at a time, so a failure only affects its own row.
2. Wrap `model(row)` in `try/except Exception`. Any error marks that row as not ok instead of escaping.
3. Define "usable" as `pred is not None and math.isfinite(pred)`. `isfinite` is false for NaN and for both infinities, so one check covers them all.
4. If the row is not ok, swap in the fallback value and count it. Either way append `{'id', 'pred', 'status'}` in order, so the output lines up with the input.
5. The rate is `n_fallback / len(rows)`, or `0.0` for an empty batch to avoid dividing by zero.

**Check it.** An empty list returns `([], 0.0)`. One pass over the rows, so linear time.

**Watch out.** Writing `if not pred` treats a legitimate prediction of `0.0` as a failure; test for `None` and finiteness explicitly.
