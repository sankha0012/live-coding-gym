**Why this matters.** Average latency hides the slow requests that users actually complain about. On-call dashboards use p95 and p99, the value that 95 or 99 percent of requests stay under.

**How we get there.**
1. `sorted(latencies)` makes a sorted copy and leaves the caller's list alone.
2. Let `n` be the length. If it is 0, every percentile is `None`.
3. For percentile `p`, the nearest rank is `ceil(p * n / 100)`, counted from 1. We compute it with integers as `-(-p * n // 100)`, so no float rounding can push us off by one.
4. Subtract 1 to get a zero-based index, and return `ordered[rank - 1]`. The answer is always an observed value.
5. Repeat for 50, 95 and 99.

**Check it.** For one value, the rank is 1 for every percentile, so it works unchanged. With 100 values, p99 is the 99th, so a single huge outlier at the end does not move it. Sorting makes it O(n log n).

**Watch out.** Rounding the rank instead of taking the ceiling, or indexing with `int(p / 100 * n)`, returns the wrong element for small lists.
