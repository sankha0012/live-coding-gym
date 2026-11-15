**Why this matters.** The standard deviation tells us how spread out the values are. The detail that matters is the divisor. We usually have a sample, and a sample sits closer to its own mean than to the true one, so we correct for that.

**How we get there.**
1. Count the values, `n = len(xs)`, and take the mean, `m = sum(xs) / n`.
2. Measure each value's distance from the mean and square it, so that negatives and positives do not cancel: `(x - m) ** 2`.
3. Add those squares and divide by `n - 1`, not `n`. This is the sample variance, and the smaller divisor makes it unbiased.
4. The standard deviation is the square root of the variance, which we write as `var ** 0.5`.
5. Return `m, var ** 0.5`.

**Check it.** For `[2, 4, 4, 4, 5, 5, 7, 9]` the mean is 5.0 and the result is about 2.1381, where dividing by `n` would give 2.0. It is one pass for the mean and one for the squares, so O(n).

**Watch out.** Dividing by `n` is the most common slip, and it quietly underestimates the spread.
