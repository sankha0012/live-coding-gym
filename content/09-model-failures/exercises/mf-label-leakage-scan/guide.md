**Why this matters.** A feature that almost equals the label usually carries information from after the prediction moment. It makes validation look great and then fails in production. A correlation scan is a cheap first alarm.

**How we get there.**
1. Write a small `_corr` helper for Pearson correlation. Centre both lists by subtracting their means.
2. Sum the squared deviations of each list and the sum of centred products. Correlation is `sxy / sqrt(sxx * syy)`.
3. Guard the denominator: if either list has zero variance, return 0.0. A constant feature, or constant labels, then never counts as leaky and nothing divides by zero.
4. In the main function, check each feature's length against `labels` and raise `ValueError` on a mismatch.
5. Keep a feature when `abs(corr) > threshold`. The absolute value matters because an inverted copy of the label leaks just as much. Store `(-c, name)`.
6. Sorting those tuples puts the highest correlation first and breaks ties by name.

**Check it.** The cost is features times rows. Exactly at the threshold does not count, since the test is strict.

**Watch out.** Using the signed correlation misses negative leaks, and skipping the zero-variance guard crashes on a constant column.
