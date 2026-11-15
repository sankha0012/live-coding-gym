---
title: Monitoring tools (Evidently, Prometheus)
summary: Watch service health and model health after deployment, because a model keeps running even when it is wrong.
tags: [ml tools, monitoring, drift]
---
- A deployed model keeps running even when it is wrong.
- Service health: request rate, error rate, latency. Prometheus collects numeric metrics and fires alerts; Grafana often draws the dashboards.
- Model health: Evidently is an open-source library that computes data and model reports.
- It sits after serving: logged inputs and predictions are compared with a reference window, usually the training data.
- Key terms: data drift, prediction drift, performance monitoring, data quality.
- Drift does not always mean the model is bad. It means look closer.

<!-- more -->

## Details

- **Data drift.** The input feature distribution changed compared with training.
- **Prediction drift.** The distribution of model outputs changed. It needs no labels, so it is a cheap early signal.
- **Performance monitoring.** Real accuracy, precision or error, once true labels arrive.
- **Data quality.** Missing values, new categories, out-of-range values, schema changes.

The Population Stability Index (PSI) is a simple drift score.

Evidently takes a reference dataframe and a current dataframe and produces a drift report. Prometheus scrapes the service's metrics endpoint, and an alert rule fires when, for example, the error rate stays high for several minutes.

Metrics tell you that something is wrong. Logs tell you why. Log structured records with the model version.

Trap: alerting on every small drift. The team learns to ignore alerts.

## What to say and what not to claim

Say: "I monitor service health with metrics like latency and error rate, and model health with input drift, prediction drift and, when labels arrive, real performance. Alerts have thresholds and an owner."

Do not claim that drift proves the model is wrong. Do not say you can detect performance loss without labels. Do not claim hands-on Evidently or Prometheus experience you do not have.

## Likely interview questions

- **How do you know a model degraded when labels come late?** Watch data drift, prediction drift and data quality early, then compute real metrics when labels arrive.
- **Data drift versus concept drift?** Data drift is a change in the inputs; concept drift is a change in the relation between inputs and target and needs labels.
- **What would you alert on?** Sustained error rate and p99 latency, large drift on key features, a jump in missing values, and a performance drop beyond an agreed limit.

## See also

- [Drift and the population stability index (PSI)](#/kb/ml-psi-drift)
- [Alerts, thresholds and hysteresis](#/kb/prod-drift-alerts-hysteresis)
- [Monitoring and latency percentiles](#/kb/prod-monitoring-percentiles)
