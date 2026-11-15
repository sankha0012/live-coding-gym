**Why this matters.** A model trained on last year's data can quietly degrade when the live inputs shift. The population stability index compares the share of traffic in each bin at training time with the share today, and gives one drift number.

**How we get there.**
1. Walk the expected and actual proportions together with `zip`, one pair per bin.
2. Zeros are a problem, because `log(a / e)` divides by zero or takes the log of zero. So we clamp both values first: `e, a = max(e, 1e-4), max(a, 1e-4)`.
3. Each bin contributes `(a - e) * math.log(a / e)`. The difference and the log always have the same sign, so a contribution is never negative.
4. Add the contributions into a running total and return it.

**Check it.** Identical distributions give exactly 0.0, since every `a - e` is zero. A bin that empties completely, such as `[0.5, 0.5]` against `[1.0, 0.0]`, gives a large score thanks to the small clamp value. Time is linear in the number of bins.

**Watch out.** Skipping the clamp crashes with a math error exactly when drift is worst, because a bin has gone to zero.
