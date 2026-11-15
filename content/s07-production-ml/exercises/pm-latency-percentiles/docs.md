# percentiles: reference

## Contract

`percentiles(latencies: list) -> dict` returns `{"p50": ..., "p95": ..., "p99": ...}` by the nearest-rank method.

- Sort the values. For percentile `p` with `n` values, the answer is the value at 1-based rank `ceil(p / 100 * n)`. The rank is rounded up, never to nearest.
- The result is always a value that appears in the input, never an interpolation. The values keep their type (int stays int, float stays float).
- The input may be unsorted and may contain duplicates. The caller's list is not modified.
- An empty list gives `None` for every key. One value gives that value for every key.

```python
percentiles([1, 2, ..., 10])   # {"p50": 5, "p95": 10, "p99": 10}
```

## Library notes

- `sorted(iterable)` returns a new list and leaves the input alone. Gotcha: `list.sort()` sorts in place and returns `None`, which would mutate the caller's list.
- `math.ceil(x)` returns an `int`. Gotcha: float arithmetic can overshoot, for example `7 / 100 * 100` is `7.000000000000001` and its ceiling is 8. Integer arithmetic such as `-(-a // b)` avoids it.
- `numpy.percentile(a, q)` returns a `float`. Gotcha: it interpolates by default, so it does not give nearest-rank results unless you pass a method argument.
- List indexing `xs[i]` is 0-based. Gotcha: rank `k` lives at index `k - 1`.

## Gotchas

- Averages hide tail latency. One slow dependency can leave the mean healthy while p99 breaks the SLA, which is why tails are tracked.
- Percentiles cannot be averaged across hosts. Merge the raw samples or histograms, then compute.
- A p99 over a handful of samples is just the maximum. Report the sample count next to it.
