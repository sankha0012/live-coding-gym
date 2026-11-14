# Monitoring: Evidently and Prometheus

## What problem it solves

A deployed model keeps running even when it is wrong. The world changes. Inputs shift, labels arrive late, an upstream table breaks. Without monitoring you find out from an angry stakeholder. ML monitoring has two layers.

- **Service health.** Is the service up, fast and error-free? Request rate, error rate, latency. This is ordinary software monitoring. Prometheus is the common tool: it collects numeric metrics and fires alerts. Grafana often draws the dashboards.
- **Model health.** Is the model still good? Evidently is an open-source library that computes data and model reports.

## What to watch

- **Data drift.** The input feature distribution changed compared with training. Example: average order value doubled.
- **Prediction drift.** The distribution of model outputs changed. It is a cheap early signal because it needs no labels.
- **Performance monitoring.** Real accuracy, precision or error, once true labels arrive. Labels are often delayed, so drift is the early warning and performance is the confirmation.
- **Data quality.** Missing values, new categories, out-of-range values, schema changes.

Drift does not always mean the model is bad. It means look closer.

## Where it sits in an ML pipeline

After serving. Logged inputs and predictions flow into a store. A scheduled job compares recent data with a reference window, usually the training data. Metrics go to Prometheus. Alerts go to the team.

## A minimal real example

The Population Stability Index (PSI) is a simple drift score. This runs on Python 3.12 with numpy.

```python
import numpy as np


def psi(reference, current, bins=5):
    edges = np.quantile(reference, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    ref = np.histogram(reference, edges)[0] / len(reference)
    cur = np.histogram(current, edges)[0] / len(current)
    ref = np.clip(ref, 1e-6, None)   # avoid log(0)
    cur = np.clip(cur, 1e-6, None)
    return float(np.sum((cur - ref) * np.log(cur / ref)))


rng = np.random.default_rng(0)
train = rng.normal(0, 1, 5000)
same = rng.normal(0, 1, 5000)
shifted = rng.normal(1, 1, 5000)

print(round(psi(train, same), 3))      # close to 0
print(round(psi(train, shifted), 3))   # much larger
```

A common rule of thumb: below 0.1 is stable, 0.1 to 0.25 is moderate, above 0.25 is a large shift. It is only a rule of thumb.

Evidently and Prometheus usage is illustrative, not run here. Check the current docs because the Evidently API has changed between versions.

```python
# Prometheus client: expose metrics from the service
from prometheus_client import Counter, Histogram

PREDICTIONS = Counter("predictions_total", "Predictions served")
LATENCY = Histogram("predict_latency_seconds", "Prediction latency")

with LATENCY.time():
    PREDICTIONS.inc()
```

Evidently takes a reference dataframe and a current dataframe and produces a drift report. Prometheus then scrapes the service's metrics endpoint, and an alert rule fires when, for example, the error rate stays high for several minutes.

## Logs

Metrics tell you that something is wrong. Logs tell you why. Log structured records: request id, model version, input summary, prediction, latency. Do not log secrets or personal data. Keep the model version in every record so you can compare versions.

## Three traps

1. Alerting on every small drift. The team learns to ignore alerts.
2. Waiting for labels before looking at anything. Use drift and data quality as early signals.
3. Comparing against the wrong reference window, such as last week's data that was already drifted.

## What to say in an interview

Say: "I monitor service health with metrics like latency and error rate, and model health with input drift, prediction drift and, when labels arrive, real performance. Alerts have thresholds and an owner."

Do NOT claim:

- That drift proves the model is wrong. It is a signal to investigate.
- That you can detect performance loss without labels. You can only estimate risk.
- Hands-on Evidently or Prometheus experience you do not have. The ideas are what matter.

## Three likely questions

**1. How do you know a model has degraded when labels come late?**
I watch data drift, prediction drift and data quality as early signals. When labels arrive I compute real metrics and compare them with the baseline.

**2. What is the difference between data drift and concept drift?**
Data drift is a change in the inputs. Concept drift is a change in the relation between inputs and the target. Data drift can be seen without labels. Concept drift needs labels.

**3. What would you alert on?**
Service alerts: error rate and p99 latency above a threshold for a sustained time. Model alerts: a large drift score on key features, a jump in missing values, and a performance drop beyond an agreed limit. Each alert needs a clear owner and action.
