A dashboard job computes metrics from raw event data. Empty windows, zero denominators and missing values must not crash it or produce NaN.

Write two functions:

- `safe_mean(values) -> float | None`: the mean of the valid numbers in `values`. `None` and `NaN` values are skipped. A valid `0` counts. If there are no valid values (including an empty list), return `None`.
- `safe_rate(successes, total) -> float | None`: `successes / total`. Return `None` if either is `None` or `NaN`, or if `total` is zero or negative.
