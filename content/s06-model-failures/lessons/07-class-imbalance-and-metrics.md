# Class imbalance and the right metric

## What it is

Class imbalance means one class is rare, such as fraud, churn or a failed delivery. Accuracy, the share of correct predictions, then misleads: if 1 percent of orders are fraud, a model that always says "not fraud" is 99 percent accurate and catches nothing. The honest metrics describe the rare class. Precision is the share of flagged cases that are truly positive. Recall is the share of true positives that were found. AUC measures how well the score ranks positives above negatives, across all thresholds. See [precision, recall and F1](#/kb/ml-metrics-precision-recall-f1) and [AUC](#/kb/ml-auc-ks).

## How it breaks in production

A dashboard shows 99 percent accuracy and everyone relaxes while the model flags nobody. Also, when a model returns no flagged rows at all, precision is 0 divided by 0, which raises an error in plain Python and a warning in scikit-learn. The metric code must handle that case. Which metric to prefer depends on cost: if a missed fraud is expensive, favour recall; if a false alarm annoys customers, favour precision.

## The defence in code

Compute the counts directly and guard the zero division. Report precision and recall together, and look at the score ranking with AUC.

```python
from sklearn.metrics import roc_auc_score

def prf(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return precision, recall

y_true = [0] * 98 + [1] * 2
always_no = [0] * 100
accuracy = sum(t == p for t, p in zip(y_true, always_no)) / 100
assert accuracy == 0.98
assert prf(y_true, always_no) == (0.0, 0.0)

scores = [0.1] * 96 + [0.9, 0.2, 0.4, 0.7]
pred = [int(s >= 0.5) for s in scores]
assert prf(y_true, pred) == (0.5, 0.5)
assert 0.5 < roc_auc_score(y_true, scores) <= 1.0
print(prf(y_true, pred))
```

## What to say in the interview

"With a rare positive class I would not report accuracy, because predicting all negatives already scores high. I would report precision and recall, choose the balance from the cost of a miss versus a false alarm, and use AUC to compare score quality independent of threshold. In the code I guard the zero-division case when nothing is flagged, so the metric function never crashes on an empty prediction."
