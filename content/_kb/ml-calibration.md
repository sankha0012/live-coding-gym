---
title: Calibration
summary: A model is calibrated when, among cases it scores near 0.7, about 70% are truly positive.
tags: [machine learning, metrics, probabilities]
---
```python
import numpy as np
y = np.array([0, 0, 0, 1,   0, 1, 0, 1,   1, 1, 1, 0])
p = np.array([0.1, 0.2, 0.2, 0.3,   0.4, 0.5, 0.5, 0.6,   0.8, 0.9, 0.9, 0.7])
edges = np.linspace(0, 1, 4)               # 3 equal bins: [0, 1/3), [1/3, 2/3), [2/3, 1]
bin_id = np.digitize(p, edges[1:-1])       # [0 0 0 0 1 1 1 1 2 2 2 2]
ece = 0.0
for b in range(3):
    m = bin_id == b                        # mean predicted vs observed rate per bin:
    ece += m.mean() * abs(p[m].mean() - y[m].mean())   # 0.2 vs 0.25, 0.5 vs 0.5, 0.825 vs 0.75
round(ece, 4)                              # 0.0417  expected calibration error
round(np.mean((p - y) ** 2), 4)            # 0.1625  Brier score
```

- Per bin, compare the mean predicted probability with the observed positive rate.
- ECE is the average gap, weighted by the share of rows in each bin. Lower is better, 0 is perfect.
- The Brier score is the mean squared error of the probabilities. Lower is better.

<!-- more -->

## Details

Calibration matters when the probability itself is used: expected loss, pricing, or any rule such as "review if risk is above 20%". Ranking metrics such as AUC do not measure it. A model can rank well and still be over-confident.

A bin where the mean prediction is above the observed rate is over-confident. In the example the top bin predicts 0.825 on average and 0.75 happen.

Worked ECE: each bin holds 4 of 12 rows, so the weight is 1/3. The gaps are 0.05, 0.0 and 0.075. ECE = (0.05 + 0.0 + 0.075) / 3 = 0.0417.

scikit-learn has the same tools:

```python
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
prob_true, prob_pred = calibration_curve(y, p, n_bins=3)
prob_true            # [0.25, 0.5, 0.75]    observed rate per bin
prob_pred            # [0.2, 0.5, 0.825]    mean prediction per bin
brier_score_loss(y, p)   # 0.1625
```

To fix calibration, wrap the model. `method="sigmoid"` (Platt scaling) fits a logistic curve and suits small data. `method="isotonic"` fits a step function and needs more data.

```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

X, Y = make_classification(n_samples=2000, n_features=10, n_informative=3,
                           n_redundant=6, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, Y, random_state=0)
raw = GaussianNB().fit(X_tr, y_tr)
cal = CalibratedClassifierCV(GaussianNB(), method="isotonic", cv=5).fit(X_tr, y_tr)
brier_score_loss(y_te, raw.predict_proba(X_te)[:, 1])    # 0.233
brier_score_loss(y_te, cal.predict_proba(X_te)[:, 1])    # 0.195
```

## Common mistakes

- Judging probabilities by AUC or accuracy. Neither measures calibration.
- Calibrating on the same rows the model was trained on. Use held-out rows or `cv`.
- Using too many bins for the data. Bins with a handful of rows give noisy rates.
- Taking the mean of an empty bin. Skip empty bins.

## See also

- [AUC and KS](#/kb/ml-auc-ks)
- [Precision, recall, F1 and accuracy](#/kb/ml-metrics-precision-recall-f1)
- [Cross-validation](#/kb/ml-cross-validation)
- Official docs: https://scikit-learn.org/stable/
