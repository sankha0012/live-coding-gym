---
title: Training-serving skew
summary: The model sees different feature values in production than in training, because two code paths compute them.
tags: [production, features, ml]
---
```python
import math

def features(raw):                  # single definition, used by training AND serving
    return {"log_amount": math.log1p(raw["amount"]), "is_weekend": raw["weekday"] >= 5}

def skew_report(train_rows, serve_rows, tol=1e-9):
    bad = []
    for i, (t, s) in enumerate(zip(train_rows, serve_rows, strict=True)):
        for name in sorted(t.keys() | s.keys()):
            a, b = t.get(name), s.get(name)
            if a is None or b is None or abs(a - b) > tol:
                bad.append((i, name, a, b))
    return bad
```

- Use it when a model is good offline and worse online with no code error.
- Key rule: one feature function for both paths, and a check that compares both on the same raw rows.
- Say: "I log the features served in production and compare them with the training pipeline's output for the same ids."

<!-- more -->

## Details

Skew is silent. Nothing raises. The model simply gets inputs from a slightly different distribution.

```python
raw = {"amount": 100.0, "weekday": 6}
train = [features(raw)]
serve = [{"log_amount": math.log(100.0), "is_weekend": True}]   # serving re-implemented it with log
[(i, name) for i, name, a, b in skew_report(train, serve)]      # [(0, 'log_amount')]
skew_report(train, train)                                       # []
```

Typical causes:

- **Duplicated logic.** Training in SQL or pandas, serving rewritten in another service.
- **Different defaults.** A missing value is 0 in training and -1, or the mean, in serving.
- **Fitted statistics.** The scaler's mean and the category list are recomputed at serving time instead of loaded from the training run.
- **Units and time.** Cents versus euros, UTC versus local time, a different "day" boundary.
- **Data availability.** Training used a value that arrives hours later in production, so serving sees it missing or stale.

Fixes, in order of strength: share one function or a feature store; save the fitted preprocessing together with the model (one pipeline artifact); log served features and compare them regularly with a tolerance.

Compare floats with a tolerance, not `==`. Treat a feature that is present on one side only as a mismatch.

## Common mistakes

- Comparing only summary statistics. Two columns can have the same mean and differ row by row.
- Using `zip` without `strict=True`, so a missing row hides at the end.
- NaN on both sides: `abs(nan - nan) > tol` is False, so it passes. Decide if that is a match and code it explicitly.
- Fixing the serving code and not retraining, when the model learned from the wrong values.
- Calling it drift. Drift is the world changing. Skew is your own two code paths disagreeing.

## See also

- [Train/test splits and data leakage](#/kb/ml-train-test-split-leakage)
- [scikit-learn Pipeline](#/kb/ml-sklearn-pipeline)
- [Drift and the population stability index (PSI)](#/kb/ml-psi-drift)
- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
