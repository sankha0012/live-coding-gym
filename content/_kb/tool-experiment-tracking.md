---
title: Experiment tracking and the model registry (MLflow)
summary: Record every training run (params, metrics, artifacts, versions) and promote named model versions through a registry.
tags: [ml tools, mlflow, model registry]
---
- Experiment tracking records every run: parameters, metrics, code version, data version and output files.
- The training code writes the record itself, so it is not forgotten or mistyped like a spreadsheet.
- It sits around training: the script logs, evaluation compares runs, and a deploy step reads the model registry.
- Key terms: run, experiment, params, metrics, artifacts, model registry.
- The registry gives a model a name, numbered versions and labels such as "production", so rollback is a change of label.

Checked against MLflow 3.18:

```python
import mlflow

mlflow.set_experiment("late-delivery-model")

with mlflow.start_run():
    mlflow.log_param("max_depth", 6)
    model.fit(X_train, y_train)
    mlflow.log_metric("auc", auc)      # computed on held-out data
```

<!-- more -->

## Details

Metrics can be logged many times, for example per epoch. Artifacts are files the run produced: the model, a plot, a report.

MLflow 3 stores runs in a local SQLite file, `mlflow.db`, by default; older versions used a folder called `mlruns`. A team points it at a shared tracking server with `mlflow.set_tracking_uri(...)`. The command `mlflow ui` opens a page where you compare runs side by side.

The registry API has changed between major versions, so check the docs for exact signatures.

Traps:

- Logging metrics measured on the training data. Log held-out metrics.
- Not logging the git commit and the data version. The run is recorded but not reproducible.
- Treating tracking as reproducibility. You still need pinned dependencies and fixed seeds.

## What to say and what not to claim

Say: "I track each run with its parameters, held-out metrics, seed, code commit and data version, and I store the model as an artifact. I promote models through a registry, so deployment points at a named version and I can roll back."

Do not claim you ran an MLflow server at scale unless you did. Do not say MLflow trains or deploys models by itself. It records and catalogues. Do not invent API calls; say you would check the docs.

## Likely interview questions

- **Why not a spreadsheet or file names?** They are manual, drift out of date and are not linked to the real model file or code.
- **What is the model registry for?** Named, versioned models with labels, so promoting or rolling back is a label change with an audit trail.
- **What makes a tracked run reproducible?** Params and metrics plus the code commit, data version, random seed and pinned environment.

## See also

- [Data and model versioning (DVC)](#/kb/tool-data-versioning)
- [CI/CD for ML](#/kb/tool-ci-cd-ml)
- [Determinism: seeds, ordering, time](#/kb/prod-determinism)
