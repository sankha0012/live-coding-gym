---
title: The bootstrap
summary: Estimate the uncertainty of any statistic by resampling the data with replacement many times.
tags: [machine learning, statistics, resampling]
---
```python
import numpy as np
rng = np.random.default_rng(0)
data = np.array([12, 15, 9, 20, 14, 11, 30, 13, 16, 10])    # mean 15.0
boot = np.array([
    rng.choice(data, size=len(data), replace=True).mean()   # one resample, same size as the data
    for _ in range(10_000)
])
boot.std()                              # 1.85   bootstrap standard error of the mean
np.percentile(boot, [2.5, 97.5])        # [11.9, 19.0]   95% confidence interval
```

- Resample with replacement, same size as the original sample.
- Compute the statistic on each resample. The spread of those values is the uncertainty.
- The 2.5th and 97.5th percentiles give a 95% interval.

<!-- more -->

## Details

The idea: the sample stands in for the population. Drawing from it with replacement imitates collecting new samples. Some rows appear twice in a resample and some not at all. That variation is the point.

The bootstrap works for statistics with no simple formula: a median, a percentile, a ratio, AUC, the difference between two models. For the mean there is a formula, and the two agree roughly: `data.std(ddof=1) / sqrt(10)` is 1.95 against the bootstrap 1.85.

A faster version draws all the indexes at once:

```python
rng = np.random.default_rng(0)
idx = rng.integers(0, len(data), size=(10_000, len(data)))   # one row of indexes per resample
np.percentile(data[idx].mean(axis=1), [2.5, 97.5])           # [11.9, 19.0]
np.percentile(np.median(data[idx], axis=1), [2.5, 97.5])     # [11.0, 17.5]  interval for the median
```

For a metric that needs pairs, such as AUC, resample row indexes and use the same indexes for labels and scores. This keeps each label with its score:

```python
i = rng.integers(0, len(data), len(data))
# metric(y_true[i], y_score[i])
```

To compare two groups, resample each group on its own, compute the difference, and look at the interval. If it excludes 0, the difference is unlikely to be chance:

```python
rng = np.random.default_rng(0)
a, b = rng.normal(10, 2, 200), rng.normal(10.5, 2, 200)
diffs = np.array([rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean()
                  for _ in range(5000)])
np.percentile(diffs, [2.5, 97.5])       # [-0.086, 0.677]  includes 0: not conclusive
```

Use a seeded generator so the interval is repeatable.

Limits: the bootstrap cannot fix a small or biased sample. It is poor for extremes such as the maximum. Rows must be independent. For time series or repeated customers, resample blocks or whole customers.

## Common mistakes

- Sampling without replacement. Every resample is then the same data and the spread is zero.
- Using a resample size different from the original, which changes the spread.
- Resampling labels and scores separately, which destroys the pairing.
- Reading the interval as covering 95% of the data. It is an interval for the statistic.
- A resample with only one class when bootstrapping AUC. Skip those resamples.

## See also

- [A/B tests and the two-proportion z-test](#/kb/ml-ab-test-z)
- [AUC and KS](#/kb/ml-auc-ks)
- [Random numbers and seeds](#/kb/py-random-seeds)
