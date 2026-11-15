Write check_batch(values, ref_mean, ref_std, max_null_rate=0.05, z=3.0) in Python, standard library only.
- Empty list -> ["empty"].
- Treat None and NaN as missing. Add "null_rate" if the missing share > max_null_rate.
- If there are valid values, add "mean_shift" if abs(mean - ref_mean) > z * ref_std / sqrt(n_valid).
- Return the alerts sorted.
Add asserts for: a healthy batch, many nulls, a shifted mean, an empty batch, all-NaN, and both alerts at once.
