## Contract

Two functions, both returning `float | None`.

`safe_mean(values) -> float | None`

- `values` is a list of numbers that may contain `None` and `NaN` (`float("nan")`).
- `None` and `NaN` are skipped. A real `0` or `0.0` is valid and counts, and negatives are valid.
- The result is the sum of the valid values divided by how many there are. With no valid values, including an empty list, it returns `None`. It never returns NaN.
- The input list is not modified.

`safe_rate(successes, total) -> float | None`

- Returns `successes / total`.
- Returns `None` if either argument is `None` or `NaN`, or if `total` is zero or negative.
- Fractional totals are legal (`safe_rate(1, 0.5) == 2.0`), the rate may be above 1, and `successes` may be 0 or negative.

Examples: `safe_mean([1.0, None, float("nan"), 3.0]) == 2.0`; `safe_rate(1, 4) == 0.25`; `safe_rate(3, 0) is None`.

## Library notes

- `math.isnan(x)` returns a bool and raises `TypeError` for `None`, so test for `None` first.
- `x != x` is True only for NaN; `float("nan") == float("nan")` is False.
- `statistics.fmean(data)` returns a float but raises `StatisticsError` on empty input, and does not skip NaN.
- `pandas.Series.mean()` skips NaN by default and returns `nan` (not `None`) when nothing is left; `numpy.nanmean` warns on all-NaN input.

## Gotchas

- `if not v` treats `0` as missing; compare with `None` explicitly.
- Comparisons with NaN are always False, so `total <= 0` does not catch a NaN total.
- One NaN that slips into a sum poisons the whole dashboard value.
