# Feature stores

## What problem it solves

Teams compute the same features many times, in different code. A data scientist builds `orders_last_7d` in a notebook for training. An engineer rewrites it in a service for prediction. The two versions differ slightly. This gap is called **training-serving skew**: the model sees one kind of feature in training and another in production. Accuracy drops and nobody knows why.

A feature store gives one place to define features, store them and read them for both training and serving.

It has two parts.

- **Offline store.** Large history, usually in a warehouse or files. Used to build training sets.
- **Online store.** Only the latest value per entity, in a fast key-value database. Used to look up features in milliseconds at prediction time.

A job copies the latest values from offline to online. This is often called materialization.

## Point-in-time correctness

When you build a training set, each row must use only the feature values that were known at that row's event time. If you join the latest value instead, you leak the future into training. The model looks great offline and fails in production.

Example: a customer placed an order on day 5. Their 7-day order count on day 5 must not include orders from day 6 and later. A good feature store does this "as of" join for you.

## Where it sits in an ML pipeline

Between raw data and the model. Data pipelines compute features and write them to the offline store. Training reads from the offline store. Serving reads from the online store. Both use the same feature definitions.

## A minimal real example

The point-in-time join is the core idea, and pandas can show it. This runs on Python 3.12 with pandas.

```python
import pandas as pd

features = pd.DataFrame({
    "customer": ["a", "a", "a"],
    "ts": pd.to_datetime(["2026-01-01", "2026-01-05", "2026-01-09"]),
    "orders_7d": [1, 3, 6],
})
labels = pd.DataFrame({
    "customer": ["a", "a"],
    "ts": pd.to_datetime(["2026-01-06", "2026-01-10"]),
    "churned": [0, 1],
})

train = pd.merge_asof(
    labels.sort_values("ts"),
    features.sort_values("ts"),
    on="ts",
    by="customer",
    direction="backward",   # only feature values at or before the label time
)
print(train)
```

The label on Jan 6 gets the Jan 5 value (3), not the Jan 9 value (6). `direction="backward"` is what prevents leakage.

Feast is a popular open-source feature store. The usage below is illustrative, not run here. It needs a configured Feast repository.

```python
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# training: point-in-time join against an entity dataframe with timestamps
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["customer_stats:orders_7d"],
).to_df()

# serving: latest values from the online store
online = store.get_online_features(
    features=["customer_stats:orders_7d"],
    entity_rows=[{"customer": "a"}],
).to_dict()
```

## Three traps

1. Joining the latest feature value into old labels. This is label leakage.
2. Using a feature store for a tiny project with one model. The cost is not worth it.
3. Forgetting to refresh the online store, so serving uses stale values.

## What to say in an interview

Say: "A feature store removes training-serving skew by sharing one definition between the offline and online paths, and it gives point-in-time correct training sets. I have used the idea of an as-of join, for example with merge_asof."

Do NOT claim:

- That a feature store is needed for every project. It pays off with many models or teams sharing features.
- That it computes features for you. You still write the feature logic. The store manages storage, retrieval and consistency.
- Production Feast experience you do not have. Say you know the concepts and the API shape.

## Three likely questions

**1. What is training-serving skew and how do you reduce it?**
It is a difference between the features seen in training and in production. I reduce it by using the same feature code or store for both, and by testing that both paths give the same value for the same entity and time.

**2. Why do you need an offline and an online store?**
They have different jobs. Offline holds history for big training reads. Online holds only the latest value for fast single lookups. One system cannot do both well.

**3. What is point-in-time correctness?**
Each training row may only use data that existed at its event time. Otherwise future information leaks in and the offline score is too optimistic. An as-of join with a backward direction enforces it.
