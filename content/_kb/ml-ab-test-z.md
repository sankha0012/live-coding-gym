---
title: A/B tests and the two-proportion z-test
summary: Test whether two conversion rates differ by more than chance, using the pooled two-proportion z-test.
tags: [machine learning, statistics, ab testing]
---
```python
import math
x_a, n_a = 200, 2000        # control: conversions, users
x_b, n_b = 250, 2000        # treatment
p_a, p_b = x_a / n_a, x_b / n_b                  # 0.10, 0.125
p_pool = (x_a + x_b) / (n_a + n_b)               # 0.1125
se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))   # 0.00999
z = (p_b - p_a) / se                             # 2.502
p_value = math.erfc(abs(z) / math.sqrt(2))       # 0.0123  two-sided
```

- Null hypothesis: both groups have the same true rate. The pooled rate estimates it.
- `abs(z) > 1.96` means a two-sided p-value below 0.05.
- The p-value is the chance of a gap at least this large if there were no real difference.

<!-- more -->

## Details

`math.erfc(abs(z) / sqrt(2))` is the two-sided p-value from the standard normal distribution, with no extra library. Halve it for a one-sided test, here 0.0062.

Sample size decides everything. The same rates with ten times fewer users are not significant:

```python
def z_test(x_a, n_a, x_b, n_b):
    p_pool = (x_a + x_b) / (n_a + n_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (x_b / n_b - x_a / n_a) / se
    return z, math.erfc(abs(z) / math.sqrt(2))

z_test(20, 200, 25, 200)       # (0.791, 0.429)
```

Report the size of the effect with a confidence interval, not only the p-value. The interval uses the unpooled standard error, because it no longer assumes the rates are equal:

```python
se_diff = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)   # 0.00998
diff = p_b - p_a                                                     # 0.025
(diff - 1.96 * se_diff, diff + 1.96 * se_diff)                       # (0.0054, 0.0446)
```

The lift is 2.5 percentage points, somewhere between 0.5 and 4.5. In relative terms it is 25%. Always say which one you mean.

The test assumes independent users, random assignment, and enough data for the normal approximation: at least about 10 conversions and 10 non-conversions per group.

Plan the sample size before the test. Small lifts need thousands of users per group.

## Common mistakes

- Checking the result every day and stopping at the first p-value below 0.05. This inflates false positives.
- Reading the p-value as "the probability that B is better". It is not.
- Calling a non-significant result "no effect". It may only mean too little data.
- Dividing by zero when `p_pool` is 0 or 1, or when a group is empty. Guard it.
- Testing many metrics or segments and reporting only the one that passed.

## See also

- [The bootstrap](#/kb/ml-bootstrap)
- [Canary, shadow and A/B assignment with stable hashing](#/kb/prod-canary-shadow-ab)
- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
