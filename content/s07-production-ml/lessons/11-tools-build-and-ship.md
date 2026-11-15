# Tools to build and ship: MLflow, FastAPI, Docker, Airflow, Pipelines, CI/CD

## What it is

Six tools an ML engineer is expected to discuss. MLflow records experiments: parameters, metrics, artifacts and a model registry. FastAPI serves a model over HTTP and validates requests with typed schemas. Docker packages the service with its exact dependencies. Airflow orchestrates dependent jobs on a schedule with retries and backfills. A scikit-learn Pipeline chains preprocessing and the model into one object. CI/CD for ML runs code, data and model checks before anything is deployed. See [pipelines](#/kb/ml-sklearn-pipeline) and [column transformers](#/kb/ml-column-transformer).

## How it breaks in production

Each tool has a catch. MLflow records what happened but does not make a run reproducible: you must also log the code commit, data version and seed. FastAPI handles HTTP, not speed; loading the model inside the handler makes every call slow. Docker fixes the environment, not the results, and secrets baked into an image leak to anyone who can pull it. Airflow schedules work, it does not compute it, and a task that appends or reads "now" is broken by a retry or a backfill. A Pipeline does not improve the model; it prevents leakage and drift between training and serving, and an unseen category crashes a default OneHotEncoder. CI catches only the failures you wrote checks for.

## The defence in code

```python
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.DataFrame({"km": [1.0, 5.0, 3.0, 8.0, 2.0, 6.0],
                   "city": ["sp", "rj", "sp", "rj", "sp", "rj"],
                   "late": [0, 1, 0, 1, 0, 1]})
pre = ColumnTransformer([("num", StandardScaler(), ["km"]),
                         ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"])])
model = Pipeline([("pre", pre), ("clf", LogisticRegression(random_state=0))])
model.fit(df[["km", "city"]], df["late"])

new = pd.DataFrame({"km": [4.0], "city": ["bh"]})     # a city never seen in training
print(model.predict_proba(new).round(2))              # works: unknown city encodes as zeros

def passes_gate(auc: float, prod_auc: float, floor: float = 0.7, tol: float = 0.01) -> bool:
    return auc >= floor and auc >= prod_auc - tol

print(passes_gate(0.74, prod_auc=0.80), passes_gate(0.81, prod_auc=0.80))
```

The Pipeline fits the scaler on training data only and accepts raw rows. The gate is the heart of ML CI: a floor, and no regression against production on a fixed holdout.

## What to say in the interview

"I use the tool for the problem, and I know its limits. MLflow for run history and a registry, with commit, data version and seed logged. FastAPI with typed validation and the model loaded once. Docker with pinned dependencies and no secrets in the image. Airflow when I need dependencies, retries and backfills, with idempotent tasks. One Pipeline for training and serving. CI gates on data and model quality. I say which I have run in production."
