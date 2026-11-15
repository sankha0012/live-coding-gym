**Why this matters.** A dashboard job meets empty windows, zero denominators and missing values every day. If it crashes, nobody sees any metrics; if it quietly prints `0` or NaN, people trust a wrong number.

**How we get there.**
1. Write one helper `_ok(v)`: true when `v is not None` and it is not a float NaN. NaN is the only float not equal to itself, so we test it with `math.isnan`.
2. For `safe_mean`, keep only the good values in a list. We test `is None`, never `if v`, because a real `0` must count.
3. If nothing is left, including an empty input, return `None`. Dividing would crash, and returning `0` would fake data.
4. Otherwise return `sum(good) / len(good)`. The divisor is the number of valid values, not the length of the input.
5. For `safe_rate`, return `None` when either argument fails `_ok` or when `total <= 0`. Otherwise `successes / total`, and a real `0` successes gives `0.0`.

**Check it.** `None` means "no data", which stays different from a true zero.

**Watch out.** Truthiness checks drop valid zeros, dividing by `len(values)` counts the missing ones, and returning `0.0` for no data hides the gap.
