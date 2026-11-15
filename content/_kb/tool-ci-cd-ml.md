---
title: CI/CD for ML
summary: Add data tests and a model validation gate to normal CI/CD, so a worse model cannot reach users quietly.
tags: [ml tools, ci-cd, validation gate]
---
- In ML a bad change can pass every code test and still ship a worse model.
- Three kinds of tests: code tests, data tests (schema, nulls, ranges, row counts) and model tests.
- CI runs on every pull request: fast code tests and data tests on a small sample.
- CD runs after merge or on a schedule: train, run the gate, register, deploy only if it passes.
- Safe rollout: shadow mode, then a canary, then full traffic.

```python
def passes_gate(new_auc: float, prod_auc: float,
                min_auc: float = 0.70, tolerance: float = 0.01) -> bool:
    # Absolute floor, and not meaningfully worse than production.
    return new_auc >= min_auc and new_auc >= prod_auc - tolerance
```

<!-- more -->

## Details

A model validation gate is a function that returns pass or fail. CI fails the job through a non-zero exit code. The production score comes from the model registry, and the evaluation set is a fixed, versioned holdout, so the comparison is fair.

In shadow mode the new model's answers are logged but not used. A canary sends it a small share of traffic. Rollback only works if the old version is still stored.

A model can improve on average and get worse for one segment, so the gate can check key segments.

## What to say and what not to claim

Say: "I treat the model as an artifact with a gate. A new model must beat a minimum score and not regress against production on a fixed holdout. I test the data too. I keep the previous version so rollback is a config change, not a retrain."

Do not say you ran fully automated retraining in production if you did not. Do not say CI can prove a model is correct. It only catches known failure types.

## Likely interview questions

- **What is different about CI for ML?** The data and the model can break things, so add data checks, a model gate, fixed seeds and a fixed holdout.
- **How do you decide automatically if a retrained model goes live?** Data checks pass, it beats a floor and is not worse than production beyond a tolerance, then shadow or canary first.
- **The new model is live and metrics drop. What do you do?** Roll back first, then investigate the data, the feature pipeline and the logs.

## See also

- [Canary, shadow and A/B assignment with stable hashing](#/kb/prod-canary-shadow-ab)
- [Experiment tracking and the model registry (MLflow)](#/kb/tool-experiment-tracking)
