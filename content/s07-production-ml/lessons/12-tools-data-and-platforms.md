# Tools for data, monitoring and LLMs: feature stores, DVC, Evidently, Prometheus, cloud, RAG

## What it is

A feature store defines each feature once and serves it from an offline store for training and an online store for low-latency lookups. DVC versions large data files and pipelines next to git, keeping a small pointer in git and the data in remote storage. Evidently computes data and model drift reports; Prometheus collects numeric service metrics and fires alerts. Cloud ML platforms (SageMaker, Vertex AI, Databricks) sell managed training, registry and endpoints. The LLM stack adds embeddings, a vector index and retrieval-augmented generation (RAG): look up relevant text, put it in the prompt and answer from it. See [chunking](#/kb/ai-chunking) and [embeddings and top-k](#/kb/ai-embeddings-topk).

## How it breaks in production

A feature store pays off with many models or teams, not one notebook. Its key trap is leakage: joining the latest value onto old labels puts the future into training, and a stale online store serves old values. DVC versions data but not parameters or code, and it does not replace quality checks. Evidently drift is a signal, not proof that the model is wrong, and Prometheus shows that something is wrong, while logs show why. Managed platforms trade convenience for lock-in, and idle endpoints still cost money. RAG reduces hallucination but does not remove it: if retrieval misses the right chunk, no prompt can fix it, so retrieval and generation need separate evaluation on a fixed test set.

## The defence in code

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
train = pd.merge_asof(labels.sort_values("ts"), features.sort_values("ts"),
                      on="ts", by="customer", direction="backward")
print(train[["ts", "orders_7d", "churned"]])
```

This is a point-in-time join. The label on January 6 receives the January 5 value (3) and not the January 9 value (6). `direction="backward"` forbids looking at the future. A feature store does this for you, and you can test it yourself with this exact shape.

## What to say in the interview

"I know these as concepts with a catch each. A feature store gives one definition for training and serving and point-in-time correct training sets, but it is not worth it for a single model. DVC ties data to a git commit. Evidently and Prometheus cover model health and service health, and drift is a prompt to investigate. Managed platforms save time and cost lock-in. For RAG I evaluate retrieval and answers separately. I say plainly which ones I have used in production."
