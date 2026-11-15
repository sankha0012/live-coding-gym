**Why this matters.** Percentiles drive latency alerts and SLOs, so a quiet off-by-one in the rank moves every number you report.

**How we get there.**
1. Run the tests. `test_one_to_hundred` fails with `p50` 51 instead of 50.
2. Reproduce: `percentiles(list(range(1, 101)))`. You get 51, 96, 100 and expect 50, 95, 99.
3. Read the rank line. `int(p / 100 * n)` is a floor, and it is used straight as a zero-based index. For p50 and n=100 that is index 50, which holds 51.
4. Nearest rank is the one-based rank `ceil(p * n / 100)`, so the index is that minus one. Integer arithmetic avoids float error: `rank = -(-p * n // 100)`, then `ordered[rank - 1]`.

**Check it.** The prompt examples: 1 to 10 gives p50 5 and p95 10; a single value returns itself.

**Watch out.** Floats can also surprise: `0.95 * n` is not always exactly representable, so integer arithmetic is safer.
