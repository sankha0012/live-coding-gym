**Why this matters.** Coupon B converted a bit better than coupon A. Is that real, or just luck from small samples? The two-proportion z-test turns the gap into a number we can compare with the usual 1.96 cutoff.

**How we get there.**
1. Compute each conversion rate: `p1 = x1 / n1` and `p2 = x2 / n2`. Their gap `p2 - p1` is the effect we measure.
2. We need to know how noisy that gap is. If both coupons are the same they share one rate, so pool them: `p = (x1 + x2) / (n1 + n2)`.
3. The standard error of the gap is `math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))`. Bigger samples shrink it.
4. The statistic is the gap divided by its error, `(p2 - p1) / se`. It says how many standard errors apart the two rates are.

**Check it.** With 120 of 1000 against 150 of 1000 we get about 1.963, and identical rates give exactly 0.0.

**Watch out.** Using each group's own `p1` and `p2` in the error, instead of the pooled `p`, is a different test, and flipping the subtraction flips the sign.
