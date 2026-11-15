**Why this matters.** Validation is the first defence before a model sees real data. A NaN that gets through usually surfaces much later, as a prediction that is NaN or a feature that is silently wrong.

**How we get there.**
1. Run the tests. One fails: `test_check_3`, the row with a NaN distance.
2. Reproduce: `validate({'distance_km': float('nan'), 'items': '4', 'hour': -1}, SCHEMA)`. The clean row still has `nan` for `distance_km`, and the issues list has no `missing:distance_km`.
3. Follow the field through the code. It is not `None`, so the missing branch is skipped. `float(nan)` works. Then `nan < lo` and `nan > hi` are both `False`, so there is no clipping either.
4. The fix goes in the first branch: treat `None` or a float NaN as missing, for example `v is None or (isinstance(v, float) and math.isnan(v))`. The solution file shows this form.
5. Run the tests again. All pass.

**Check it.** `math` is imported in the buggy file but never used. A helper that is imported and not used is a hint that a check was dropped.

**Next time.** For any numeric validation, add NaN to the list of inputs next to `None`, zero and the boundaries.

**Watch out.** Do not rely on `v == v` tricks without a comment; `math.isnan` says what it means.
