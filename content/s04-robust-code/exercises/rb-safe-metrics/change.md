Change: a default for empty windows. Give `safe_mean` an optional second parameter `default=None`, so the signature is `safe_mean(values, default=None)`.

When there are no valid values (an empty list, or only `None` and `NaN`), return `default` instead of `None`. For example, `safe_mean([], 0.0)` returns `0.0` and `safe_mean([None, float("nan")], default=-1)` returns `-1`. When there are valid values the result is the mean as before, and `default` is ignored. `safe_rate` does not change.

Do this by hand in your own passing solution. It should take two lines.
