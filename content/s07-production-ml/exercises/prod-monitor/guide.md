**Why this matters.** Most model incidents start upstream: a feed fills with nulls, or a unit changes. Cheap checks on each batch catch that early.

**How we get there.**
1. An empty batch has nothing to measure, so we return `["empty"]` right away.
2. Build the valid values: those that are not `None` and not `math.isnan`. The `nan` test is needed because `nan` is a float and slips past a `None` check.
3. The null rate is `1 - len(valid) / len(values)`. If it is above `max_null_rate`, add `"null_rate"`.
4. Only if there are valid values, compare their mean to `ref_mean`. The allowed gap is `z * ref_std / math.sqrt(len(valid))`, the standard error, so small batches do not raise false alarms. A larger gap adds `"mean_shift"`.
5. Return `sorted(alerts)` so the order is always the same.

**Check it.** A batch of only nulls gives `["null_rate"]` and skips the mean, which would divide by zero. One pass, so linear cost. Exactly 1 null in 20 still alerts at the default 5%, because `1 - 19/20` is `0.05000000000000004`.

**Watch out.** Computing the mean over a list that still holds `None` or `nan` crashes or returns `nan`, which silently never alerts.
