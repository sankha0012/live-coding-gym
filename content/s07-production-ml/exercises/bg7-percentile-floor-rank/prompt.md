Write `percentiles(latencies: list) -> dict` that returns `{"p50": ..., "p95": ..., "p99": ...}` using the nearest-rank method.

Nearest rank: sort the values, then for percentile `p` take the value at 1-based rank `ceil(p / 100 * n)`, where `n` is the number of values. Return a real value from the list, never an interpolated one. For `[1, 2, ..., 100]`, p95 is `95`. For `[1, 2, ..., 10]`, p50 is `5` and p95 is `10`.

- The input may be in any order. Do not change the caller's list.
- An empty list returns `{"p50": None, "p95": None, "p99": None}`.
- A list with one value returns that value for every percentile.

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
