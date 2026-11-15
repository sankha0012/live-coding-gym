# Statistics by hand

## What it is

The interview may ask you to compute mean, standard deviation, z-score, percentiles and AUC without a library, or to explain what the library does. These formulas also drive monitoring: z-scores for anomalies, percentiles for latency, AUC for ranking quality. See [AUC and KS](#/kb/ml-auc-ks), [bootstrap](#/kb/ml-bootstrap) and [percentiles in monitoring](#/kb/prod-monitoring-percentiles).

## How it breaks in production

- **Population or sample.** `np.std` divides by n and `pd.Series.std` divides by n minus 1. The same data gives 2.0 and 2.14.
- **Percentile definitions.** Libraries interpolate between values by default. Picking `sorted(v)[int(0.9 * n)]` by hand gives another number.
- **Constant data.** A standard deviation of zero makes every z-score a division by zero.
- **AUC with ties.** Equal scores must count as half a win, and AUC needs both classes present.

## The defence in code

```python
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

v = [2, 4, 4, 4, 5, 5, 7, 9]
mean = sum(v) / len(v)
std = (sum((a - mean) ** 2 for a in v) / len(v)) ** 0.5
print(mean, std, np.std(v), round(np.std(v, ddof=1), 2), round(pd.Series(v).std(), 2))
print((7 - mean) / std)                          # z-score of 7: 1.0
print(np.percentile(v, 90), sorted(v)[int(0.9 * len(v))])   # 7.6 9

def auc(y, s):
    s, y = np.asarray(s), np.asarray(y)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        raise ValueError("AUC needs both classes")
    wins = (pos[:, None] > neg).sum() + 0.5 * (pos[:, None] == neg).sum()
    return wins / (len(pos) * len(neg))

y, s = [0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]
print(auc(y, s), roc_auc_score(y, s))             # 0.75 0.75
print(auc([0, 1], [0.5, 0.5]))                    # 0.5
```

The mean is 5, the population standard deviation is exactly 2.0, and the sample one is about 2.14, so I say which I use. The z-score of 7 is 1.0. The linear-interpolated 90th percentile is 7.6, while the naive index gives 9. AUC is the share of positive-negative pairs where the positive scores higher, with ties counted as half. It gives 0.75, matching scikit-learn, and 0.5 for all-equal scores. It is O(n_pos times n_neg), fine for an interview and too slow for millions of rows.

## What to say in the interview

"I state the definition before I compute: population or sample standard deviation, and how percentiles are interpolated. I guard the zero-variance and single-class cases. AUC is the probability that a random positive scores above a random negative, with ties counted as half, and I can check my version against scikit-learn on a small example."
