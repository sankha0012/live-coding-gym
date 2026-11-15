---
title: Feature stores
summary: One place to define, store and read features for both training and serving, with point-in-time correct training sets.
tags: [ml tools, feature store, training-serving skew]
---
- Teams compute the same feature twice, in a notebook for training and in a service for prediction, and the versions differ.
- That gap is training-serving skew. A feature store gives one definition used by both paths.
- It sits between raw data and the model: training reads the offline store, serving reads the online store.
- Key terms: offline store, online store, materialization, point-in-time correctness.
- You still write the feature logic. The store manages storage, retrieval and consistency.

```python
train = pd.merge_asof(
    labels.sort_values("ts"),
    features.sort_values("ts"),
    on="ts",
    by="customer",
    direction="backward",   # only feature values at or before the label time
)
```

<!-- more -->

## Details

- **Offline store.** Large history, usually in a warehouse or files. Used to build training sets.
- **Online store.** Only the latest value per entity, in a fast key-value database. Used for lookups in milliseconds at prediction time.

A job copies the latest values from offline to online. This is often called materialization.

**Point-in-time correctness.** Each training row must use only the feature values known at that row's event time. If you join the latest value instead, you leak the future into training. A good feature store does this "as of" join for you. In pandas, `merge_asof` with `direction="backward"` shows the same idea.

Feast is a popular open-source feature store.

Traps:

- Using a feature store for a tiny project with one model. The cost is not worth it.
- Forgetting to refresh the online store, so serving uses stale values.

## What to say and what not to claim

Say: "A feature store removes training-serving skew by sharing one definition between the offline and online paths, and it gives point-in-time correct training sets."

Do not claim a feature store is needed for every project. It pays off with many models or teams sharing features. Do not claim production Feast experience you do not have.

## Likely interview questions

- **What is training-serving skew and how do you reduce it?** A difference between training and production features; use the same feature code or store for both and test that both paths agree.
- **Why an offline and an online store?** Offline holds history for big training reads; online holds the latest value for fast single lookups.
- **What is point-in-time correctness?** A training row may only use data that existed at its event time; a backward as-of join enforces it.

## See also

- [Training-serving skew](#/kb/prod-train-serve-skew)
- [Time-based splits and leakage](#/kb/pd-time-split-leakage)
- [Model serving: batch versus online, FastAPI](#/kb/tool-model-serving)
