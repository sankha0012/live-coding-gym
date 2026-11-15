---
title: AUC and KS
summary: Two threshold-free measures of how well a score ranks positives above negatives.
tags: [machine learning, metrics, ranking]
---
```python
import numpy as np
y = np.array([1, 1, 0, 1, 0, 0, 1, 0])
s = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.1])   # model scores, already sorted high to low
pos, neg = s[y == 1], s[y == 0]
wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)   # 12 of 16 pairs
auc = wins / (len(pos) * len(neg))                       # 0.75

tpr = np.cumsum(y) / y.sum()               # [0.25, 0.5, 0.5, 0.75, 0.75, 0.75, 1.0, 1.0]
fpr = np.cumsum(1 - y) / (1 - y).sum()     # [0.0, 0.0, 0.25, 0.25, 0.5, 0.75, 0.75, 1.0]
ks = (tpr - fpr).max()                     # 0.5, reached at score 0.8
```

- AUC is the chance that a random positive scores higher than a random negative. 0.5 is random, 1.0 is perfect.
- KS is the largest gap between the cumulative share of positives and of negatives. 0 is no separation, 1 is perfect.
- Both use only the order of the scores, not their values.

<!-- more -->

## Details

AUC means area under the ROC curve. The ROC curve plots the true positive rate (recall) against the false positive rate for every threshold. The pair-counting formula above gives the same number as the area. Ties count as half a win.

KS is the Kolmogorov-Smirnov statistic between the score distribution of the positives and of the negatives. To compute it, sort by score from high to low, accumulate the share of positives (`tpr`) and of negatives (`fpr`), and take the largest difference. The score where it happens is the threshold that separates the classes best.

The arrays above are already sorted. For unsorted data, sort first with `order = np.argsort(-s)` and use `y[order]`.

The same numbers with scikit-learn:

```python
from sklearn.metrics import roc_auc_score, roc_curve
roc_auc_score(y, s)                  # 0.75
fpr_c, tpr_c, thresholds = roc_curve(y, s)
(tpr_c - fpr_c).max()                # 0.5   KS
thresholds[np.argmax(tpr_c - fpr_c)] # 0.8
```

Useful facts:

- Gini is `2 * AUC - 1`. Here 0.5.
- Any change that keeps the order leaves both metrics unchanged: `roc_auc_score(y, s * 100)` is still 0.75.
- Reversed scores give `1 - AUC`: `roc_auc_score(y, 1 - s)` is 0.25. An AUC well below 0.5 usually means a flipped label or sign.
- Neither says anything about calibration. A model can rank perfectly and still output wrong probabilities.

## Common mistakes

- Passing hard 0/1 predictions instead of scores. `roc_auc_score(y, (s >= 0.5).astype(int))` gives 0.625, not 0.75.
- Passing `predict_proba(X)` whole. Use the positive column: `predict_proba(X)[:, 1]`.
- Mixing up this KS with the drift KS, which compares one feature across two time periods.

## See also

- [Precision, recall, F1 and accuracy](#/kb/ml-metrics-precision-recall-f1)
- [Calibration](#/kb/ml-calibration)
- [Drift and the population stability index (PSI)](#/kb/ml-psi-drift)
- Official docs: https://scikit-learn.org/stable/
