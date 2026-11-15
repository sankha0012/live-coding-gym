**Why this matters.** We have one sample and want to know how much its mean would wobble with a different sample. The bootstrap answers this by pretending the sample is the population: resample from it many times and see how the mean moves.

**How we get there.**
1. Call `random.seed(seed)` first, so the same inputs always give the same interval.
2. One resample is `random.choices(xs, k=n)`. That draws `n` values with replacement, the same size as the original sample.
3. Take its mean, `sum(...) / n`. Repeat this `B` times and sort the means.
4. The 95% interval leaves 2.5% on each side. So the low end is the value at position `int(0.025 * B)`, and the high end is at `int(0.975 * B) - 1`. The `-1` makes it zero-based: with `B=1000` the bounds are positions 25 and 974, leaving 25 means outside on each side.
5. Return the two values as `(low, high)`.

**Check it.** The interval should usually contain the sample mean, and more resamples make it steadier. The cost is O(B * n) plus the sort.

**Watch out.** Sampling without replacement (`random.sample`) just reshuffles the data, so every mean is identical and the interval collapses to a point.
