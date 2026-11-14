# CI/CD for ML

## The problem it solves

In normal software, a bad change breaks a test. In ML, a bad change can pass every test and still ship a worse model. The data changed, the labels shifted, or a new feature has nulls, and nothing crashed. CI/CD for ML adds checks for data and for model quality, so a bad model cannot reach users quietly.

Think of three kinds of tests:

- Code tests: unit tests for your functions, as in any project.
- Data tests: the schema is right, no unexpected nulls, values in range, enough rows.
- Model tests: the new model is good enough, and not worse than the one in production.

## Where it sits in an ML pipeline

CI runs on every pull request. It runs the fast code tests and the data tests on a small sample.

CD (or a training pipeline) runs after merge or on a schedule. It trains the model, runs the validation gate, registers the model, and deploys it only if the gate passes. Retraining can be automated: on a schedule (every week), or on a trigger (drift detected, new data arrived).

Rollback means you keep the previous model version. If the new one misbehaves in production, you point serving back to the old version. This only works if models are versioned and the old one is still stored.

A common safe rollout: shadow mode first (new model runs, answers are logged but not used), then a canary (a small share of traffic), then full traffic.

## A minimal real example

A model validation gate is just a function that returns pass or fail, and CI fails the job when it returns fail. Below is a gate with a data check and a model check. It runs as is.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def check_data(df: pd.DataFrame) -> list[str]:
    problems = []
    if len(df) < 100:
        problems.append("too few rows")
    if df["target"].isna().any():
        problems.append("target has nulls")
    if not df["age"].between(0, 120).all():
        problems.append("age out of range")
    return problems


def passes_gate(new_auc: float, prod_auc: float,
                min_auc: float = 0.70, tolerance: float = 0.01) -> bool:
    # Absolute floor, and not meaningfully worse than production.
    return new_auc >= min_auc and new_auc >= prod_auc - tolerance


rng = np.random.default_rng(0)
df = pd.DataFrame({"age": rng.integers(18, 80, 500)})
df["target"] = (df["age"] + rng.normal(0, 15, 500) > 50).astype(int)

assert check_data(df) == []

X_tr, X_te, y_tr, y_te = train_test_split(
    df[["age"]], df["target"], test_size=0.3, random_state=0
)
model = LogisticRegression().fit(X_tr, y_tr)
auc = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])
print(round(auc, 3), passes_gate(auc, prod_auc=0.75))
```

In a real pipeline, `prod_auc` comes from the model registry, and the evaluation set is a fixed, versioned holdout, so the comparison is fair. The job runs in GitHub Actions, GitLab CI or Jenkins. The workflow file only calls your script, for example `python -m pytest` and then `python validate.py`. A non-zero exit code fails the pipeline. (The workflow file itself is illustrative, not run here.)

Tests for the gate are cheap and valuable: test that `passes_gate` rejects a model that is worse than production, and that `check_data` catches a null target.

## What to say in an interview

- "I treat the model as an artifact with a gate. A new model must beat a minimum score and not regress against production on a fixed holdout."
- "I test the data too: schema, nulls, ranges, row counts. Most ML incidents start in the data."
- "I keep the previous model version so rollback is a config change, not a retrain."
- Mention slicing: a model can improve on average and get worse for one segment, so the gate can check key segments.
- Mention determinism: seeds fixed, data and code versions recorded, so a run can be reproduced.

What NOT to claim:

- Do not say you ran fully automated retraining in production if you did not. Say you know how it is designed.
- Do not say CI can prove a model is correct. It only catches known failure types.
- Do not name tools you have not used as if you had. It is fine to say "for example GitHub Actions" as an example of the idea.

## Three likely questions

**1. What is different about CI for ML compared to normal software?**
Besides code, the data and the model can break things. So I add data checks and a model validation gate. Results can also change with data, so I fix seeds and use a fixed holdout to make runs comparable.

**2. How would you decide automatically if a retrained model goes live?**
It must pass data checks, beat an absolute floor, and not be worse than production by more than a small tolerance on the same holdout, also on key segments. If it passes, it goes to shadow or canary first. If it fails, production keeps the old model and someone is alerted.

**3. The new model is live and metrics drop. What do you do?**
First roll back to the previous version, because users come first. Then investigate: compare input data to training data, check for a feature pipeline change, and check the logs. Fix, retrain, and pass the gate again before redeploying.
