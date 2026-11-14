# Cloud ML platforms: SageMaker, Vertex AI, Databricks

## The problem they solve

Training and serving models needs machines, storage, security, scheduling and monitoring. Building all of that yourself is slow. A cloud ML platform sells you these parts as managed services, so a team spends its time on the model and not on servers.

You do not need to know every feature. You need to know what each platform is for, and speak about it honestly.

## What each one gives you

**Amazon SageMaker** (AWS): managed notebooks, training jobs on rented machines, a model registry, real-time endpoints and batch jobs for serving, pipelines, and monitoring. You pay for the compute you use. It fits teams that already live in AWS.

**Vertex AI** (Google Cloud): the same family of ideas on Google Cloud: managed training, a model registry, endpoints for serving, pipelines, and access to Google's hosted models. It connects well with BigQuery for data.

**Databricks**: built around Apache Spark and a "lakehouse", which means data in files on cloud storage with table features on top. It is strong for large data processing, notebooks shared by a team, and it includes MLflow for experiment tracking and a model registry. It runs on top of AWS, Azure or Google Cloud.

Shared pattern across all three: data lives in cloud storage, a job trains the model on a rented machine and then the machine goes away, the model is stored in a registry, and an endpoint serves it.

## Where they sit in an ML pipeline

They cover most of the pipeline: data preparation (Databricks especially), training, registry, deployment, and monitoring. You can use only a part, for example only the training jobs, and keep serving elsewhere.

The key tradeoff is convenience against lock-in and cost. Managed services save time but tie you to one vendor's APIs, and idle endpoints still cost money.

## A minimal real example

The idea behind a managed training job is: your training script stays plain, and the platform runs it somewhere else. Make your script platform-friendly and it works everywhere: read paths and settings from arguments, write the model to an output folder.

```python
import argparse
import json
import tempfile
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression


def train(output_dir: str, c: float) -> None:
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 3))
    y = (X[:, 0] > 0).astype(int)
    model = LogisticRegression(C=c, random_state=0).fit(X, y)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out / "model.joblib")
    (out / "metrics.json").write_text(json.dumps({"train_acc": model.score(X, y)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=tempfile.mkdtemp())
    parser.add_argument("--c", type=float, default=1.0)
    args = parser.parse_args()
    train(args.output_dir, args.c)
    print("saved to", args.output_dir)
```

A platform job takes exactly this kind of script, a machine type, and input and output locations, and runs it for you. The submit call is different on each platform, so I do not show it here: look it up in the docs rather than memorise it.

## What to say in an interview

- Be honest about your level. A good line: "I have built and run the pipeline pieces locally and with open-source tools. I have not run production workloads on SageMaker, but I understand what it manages and I would read its docs to map my pipeline onto it."
- Explain the concepts, not the buttons: managed training, registry, endpoint, batch versus online serving, autoscaling, cost.
- Show judgment: when is managed worth it, when is a simple container on a VM enough, what could lock you in.
- Mention cost control: stop idle endpoints, use batch when latency does not matter, set budgets and alerts.
- Mention security basics: least-privilege access, no secrets in code, data staying in your own account or region.

What NOT to claim:

- Do not say you have used a platform if you have only read about it. Interviewers ask one follow-up and it shows.
- Do not list services by name to sound broad. Pick the ideas you can explain.
- Do not say one platform is "the best". They overlap a lot, and the right choice depends on where the data and the team already are.

## Three likely questions

**1. When would you use a managed platform instead of your own servers?**
When the team is small, the work is bursty, and time to production matters more than fine control. Managed training and endpoints remove a lot of operations work. I would think twice if costs are high and steady, or if lock-in is a risk.

**2. What is the difference between batch and online prediction there?**
Online is an endpoint that answers one request in milliseconds and costs money while it runs. Batch scores a big table on a schedule and writes results to storage. If the business does not need an answer instantly, batch is cheaper and simpler.

**3. Have you used SageMaker (or Vertex, or Databricks)?**
Answer with the truth. For example: "Not in production. I know it manages training jobs, a registry and endpoints, and I have built the same steps with scikit-learn, joblib and a container. I can map them across quickly." Honest and specific is better than a vague yes.
