---
title: Precision, recall, F1 and accuracy
summary: Count true and false positives and negatives, then turn them into precision, recall, F1 and accuracy.
tags: [machine learning, metrics, classification]
---
```python
y_true = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
y_pred = [1, 1, 1, 0, 1, 1, 0, 0, 0, 0]
pairs = list(zip(y_true, y_pred))
tp = sum(t == 1 and p == 1 for t, p in pairs)   # 3  predicted 1, really 1
fp = sum(t == 0 and p == 1 for t, p in pairs)   # 2  predicted 1, really 0
fn = sum(t == 1 and p == 0 for t, p in pairs)   # 1  predicted 0, really 1
tn = sum(t == 0 and p == 0 for t, p in pairs)   # 4
precision = tp / (tp + fp)                      # 0.6    of predicted positives, how many are right
recall = tp / (tp + fn)                         # 0.75   of real positives, how many were found
f1 = 2 * precision * recall / (precision + recall)   # 0.667
accuracy = (tp + tn) / len(y_true)              # 0.7
```

- Precision divides by what the model predicted positive. Recall divides by what is truly positive.
- F1 is the harmonic mean of the two. It is low if either one is low.
- Accuracy is misleading when one class is rare.

<!-- more -->

## Details

scikit-learn gives the same numbers. The argument order is always `(y_true, y_pred)`:

```python
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
precision_score(y_true, y_pred)     # 0.6
recall_score(y_true, y_pred)        # 0.75
f1_score(y_true, y_pred)            # 0.666...
accuracy_score(y_true, y_pred)      # 0.7
confusion_matrix(y_true, y_pred)    # [[4, 2], [1, 3]]  rows = true, columns = predicted
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
```

The matrix layout is `[[tn, fp], [fn, tp]]`, with class 0 first.

Why accuracy fails on imbalanced data: with 99 negatives and 1 positive, a model that always says 0 has accuracy 0.99 and recall 0.0.

Guard the divisions. When the model predicts no positives, `tp + fp` is 0. Return 0.0 in that case. scikit-learn does the same and warns unless you pass `zero_division=0`.

These metrics need hard 0/1 predictions, so they depend on the threshold applied to the score:

```python
import numpy as np
proba = np.array([0.9, 0.8, 0.6, 0.4, 0.7, 0.55, 0.45, 0.2, 0.1, 0.1])
pred_low = (proba >= 0.35).astype(int)
precision_score(y_true, pred_low), recall_score(y_true, pred_low)   # (0.571..., 1.0)
```

Lowering the threshold from 0.5 to 0.35 raised recall from 0.75 to 1.0 and cut precision from 0.6 to 0.571. Missing fraud is a false negative: favour recall. Blocking a good customer is a false positive: favour precision.

## Common mistakes

- Swapping the two: precision has `fp` in the denominator, recall has `fn`.
- Passing arguments as `(y_pred, y_true)`. Precision and recall swap silently.
- Passing probabilities to `precision_score`. Apply a threshold first.

## See also

- [AUC and KS](#/kb/ml-auc-ks)
- [Calibration](#/kb/ml-calibration)
- [Cross-validation](#/kb/ml-cross-validation)
- Official docs: https://scikit-learn.org/stable/
