# Train and serving skew

## What it is

Training-serving skew means the model sees different feature values in production than it saw in training for the same real-world situation. The usual cause is two code paths: a notebook or batch job computes features for training, and a separate service reimplements them for serving. The two drift apart by small differences. See [train-serving skew](#/kb/prod-train-serve-skew).

## How it breaks in production

Offline metrics look excellent, online results are worse, and no exception is raised. Typical culprits are a different fill value for missing data (mean in training, zero in serving), a different rounding or unit (seconds versus milliseconds), a different category order in one-hot encoding, a scaler fitted on training data and not saved, or a time window that includes the future offline but not online. Each one shifts the inputs a little, and the model, which learned from the training version, misreads them. Because the code on both sides is "correct" in isolation, only a comparison reveals the bug.

## The defence in code

The strongest defence is a single feature function used by both paths. The second is a test that runs the same raw rows through both paths and compares the outputs. See also [sklearn pipelines](#/kb/ml-sklearn-pipeline).

```python
import math

def features(raw):
    # shared by training and serving: one definition, one place to fix
    amount = raw.get("amount")
    amount = 0.0 if amount is None else float(amount)
    return {"amount": amount, "log_amount": math.log1p(amount)}

def serving_features_v1(raw):
    # a copy that drifted: it forgets the None default
    return {"amount": raw["amount"], "log_amount": math.log1p(raw["amount"])}

rows = [{"amount": 10}, {"amount": None}]

def compare(path_a, path_b, rows):
    diffs = []
    for r in rows:
        try:
            a, b = path_a(r), path_b(r)
        except Exception as e:
            diffs.append((r, type(e).__name__))
            continue
        if a != b:
            diffs.append((r, a, b))
    return diffs

assert compare(features, features, rows) == []
bad = compare(features, serving_features_v1, rows)
assert len(bad) == 1
print(bad)
```

In real systems the comparison runs on logged serving rows against the training pipeline, with a tolerance for floats. Also save the fitted artefacts (scalers, encoders) with the model and load the same ones at serving time.

## What to say in the interview

"If offline is good and online is worse with no errors, I suspect skew first. I would make training and serving call the same feature function, and I would add a test that feeds the same raw rows through both paths and compares the output. I would also persist the fitted scaler and encoder with the model. If two implementations must exist, I would log serving features and compare their distributions to training."
