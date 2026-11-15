---
title: Drift and the population stability index (PSI)
summary: PSI compares the binned distribution of a feature or score between a baseline and a new period.
tags: [machine learning, drift, monitoring]
---
```python
import numpy as np
expected = np.array([0.25, 0.25, 0.25, 0.25])   # share of rows per bin at training time
actual = np.array([0.10, 0.20, 0.30, 0.40])     # share per bin now, same bin edges
terms = (actual - expected) * np.log(actual / expected)
terms.round(4)          # [0.1374, 0.0112, 0.0091, 0.0705]
terms.sum()             # 0.2282
```

- PSI = sum over bins of `(actual - expected) * ln(actual / expected)`.
- Every term is zero or positive. PSI is 0 when the two distributions are identical.
- Rule of thumb: below 0.1 stable, 0.1 to 0.25 moderate shift, above 0.25 large shift.

<!-- more -->

## Details

Drift means the data the model sees in production no longer looks like the training data. PSI measures it for one variable at a time: a feature, or the model score. It needs no labels.

Steps for a numeric variable:

1. Choose bin edges on the baseline, usually deciles.
2. Count the share of baseline rows and of new rows in each bin, using the same edges.
3. Replace zero shares with a small number, then apply the formula.

```python
def psi(expected, actual, bins=10, eps=1e-6):
    edges = np.quantile(expected, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf            # catch values outside the baseline range
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, eps, None), np.clip(a, eps, None)   # no log(0), no division by zero
    return float(np.sum((a - e) * np.log(a / e)))

rng = np.random.default_rng(0)
base = rng.normal(0, 1, 5000)
psi(base, rng.normal(0, 1, 5000))      # 0.0055  same distribution
psi(base, rng.normal(0.3, 1, 5000))    # 0.0976  mean moved by 0.3 standard deviations
psi(base, rng.normal(1, 1, 5000))      # 0.9428  mean moved by 1 standard deviation
```

Worked term from the brief: the first bin went from 0.25 to 0.10. `(0.10 - 0.25) * ln(0.10 / 0.25)` = `-0.15 * -0.9163` = 0.1374.

For a categorical variable the categories are the bins. Take the union of the categories from both periods. A category that is new in production has an expected share of 0, which is why the `eps` clip is needed.

PSI is noisy on small samples. Comparing the baseline with only 100 fresh rows from the same distribution gave 0.13 here.

## Common mistakes

- Computing new bin edges on the new data. The edges must come from the baseline.
- Not handling an empty bin. The log of 0 gives `inf` or `nan`.
- Leaving the outer edges at the baseline minimum and maximum, so new extreme values fall outside every bin.
- Treating a high PSI as proof the model is worse. It says the inputs moved. Check the performance metrics when labels arrive.

## See also

- [AUC and KS](#/kb/ml-auc-ks)
- [Calibration](#/kb/ml-calibration)
- [Alerts, thresholds and hysteresis](#/kb/prod-drift-alerts-hysteresis)
- [Training-serving skew](#/kb/prod-train-serve-skew)
