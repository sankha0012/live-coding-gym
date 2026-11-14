# Experiment tracking with MLflow

## What problem it solves

You train a model on Monday with learning rate 0.1. On Thursday you try 0.05 and a new feature. On Friday your manager asks which run gave the 0.82 AUC and how to reproduce it. If you kept notes in a spreadsheet or in file names like `model_final_v3_REAL.pkl`, you probably cannot answer.

Experiment tracking records every run: the parameters, the metrics, the code version, the data version and the output files. The record is written by the code itself, so it is not forgotten and not typed wrong.

A spreadsheet fails because it is manual, it gets out of date, it has no link to the real model file, and two people editing it overwrite each other. A tracking server is shared, searchable and tied to the artifacts.

## Where it sits in an ML pipeline

It sits around training. The training script logs to a tracking store. Later steps read from it: evaluation compares runs, and a deploy step picks the chosen model from the model registry.

The MLflow words you should know:

- **Run**: one execution of training code.
- **Experiment**: a named group of runs, for example "late-delivery-model".
- **Params**: inputs you set, such as `max_depth`.
- **Metrics**: numbers you measure, such as `auc`. They can be logged many times, for example per epoch.
- **Artifacts**: files the run produced, such as the model, a plot or a report.
- **Model registry**: a catalogue of named models with versions and stages or aliases, such as "candidate" or "production". It lets a deploy job ask for "the production version of the late model" without knowing a file path.

## A minimal real example

Illustrative, not run here. MLflow is not installed in this project, and these are the common calls.

```python
import mlflow
import mlflow.sklearn

mlflow.set_experiment("late-delivery-model")

with mlflow.start_run():
    mlflow.log_param("max_depth", 6)
    model.fit(X_train, y_train)                    # your scikit-learn model
    mlflow.log_metric("auc", auc)                  # computed on held-out data
    mlflow.sklearn.log_model(model, "model")       # name of the artifact path; newer versions may rename this argument. Saves the model as an artifact
```

By default MLflow writes to a local folder called `mlruns`. In a team you point it at a shared tracking server with `mlflow.set_tracking_uri(...)`. The command `mlflow ui` opens a web page where you compare runs side by side.

To register a model you can pass `registered_model_name="late-delivery"` to `log_model`, or register a logged model afterwards. Check the docs for the exact signature of the version you use, because the registry API has changed between major versions.

The same idea works with other tools. Weights & Biases, Comet and the cloud platforms all offer run tracking with the same concepts.

## The traps

- Logging metrics measured on the training data and calling them results. Log held-out metrics.
- Forgetting to log the data version and the code version. Then the run is recorded but not reproducible. Log a git commit and a data hash or path as params or tags.
- Treating tracking as reproducibility. It records what happened. You still need pinned dependencies and fixed seeds to repeat it.
- Logging a random seed only sometimes. Always log it.

## What to say in an interview

Say: "I track each run with its parameters, metrics, code commit and data version, and I store the model as an artifact. I promote models through a registry so deployment points at a named version, and I can roll back."

Say what you would log: parameters, held-out metrics, seed, data version, git commit, environment.

Do NOT claim you ran an MLflow server at scale, or configured its backend database and artifact storage, unless you did. Do NOT say it trains or deploys models by itself. It records and catalogues; other tools train and serve. Do NOT invent flag names or API calls you are unsure of; say you would check the docs.

## Three likely questions

**1. Why not just use a spreadsheet or file names?**
They are manual and drift out of date. They are not linked to the real model file or the code that made it, and they do not scale to a team. Tracking is automatic, searchable, shared and tied to artifacts.

**2. What is the model registry for?**
It gives each model a name and numbered versions, plus labels like "staging" or "production". Deployment asks for the production version by name, so promoting or rolling back is a change of label, not a file copy. It also keeps an audit trail of who promoted what.

**3. What would make a tracked run reproducible?**
The params and metrics alone are not enough. I also need the code commit, a data version, the random seed and the pinned environment, for example a container image. With those I can rerun and expect the same result.
