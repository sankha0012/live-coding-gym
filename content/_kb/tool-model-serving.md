---
title: "Model serving: batch versus online, FastAPI"
summary: Serving turns a model file into a service with a stable contract, either as a scheduled batch job or a live API.
tags: [ml tools, serving, fastapi]
---
- A trained model is a file. Serving turns it into a service with a stable contract: this input in, this output out.
- Online serving: one request, one prediction, in milliseconds. Use it when a user waits.
- Batch serving: a scheduled job scores many rows and writes them to a table. Use it when nobody waits.
- Batch is simpler, cheaper and easier to test. Choose online only when the answer needs fresh data or a live user action.
- It is the last step before the consumer.
- FastAPI is a Python web framework that validates requests with pydantic types and writes API docs for you.

Checked with FastAPI's test client (imports left out; a negative distance returns 422):

```python
app = FastAPI()
model = joblib.load("model.joblib")   # load once, not per request


class Order(BaseModel):
    distance_km: float = Field(gt=0)
    items: int = Field(ge=1)


@app.post("/v1/predict")
def predict(order: Order):
    pred = model.predict([[order.distance_km, order.items]])[0]
    return {"minutes": float(pred), "model_version": "2026-11-01"}
```

<!-- more -->

## Details

Bad input, such as a negative distance, is rejected with a 422 error before your code runs.

- **Request validation.** Check types, ranges and required fields at the boundary.
- **Health checks.** Liveness says the process is up. Readiness says the model is loaded and the service can take traffic.
- **Latency.** Load the model at startup, not inside the request handler. Measure p50 and p99.
- **Versioned endpoints.** Put a version in the path and return the model version in the response.
- **Same preprocessing.** Different preprocessing in serving than in training makes predictions quietly go wrong.

## What to say and what not to claim

Say: "I would choose batch unless the use case needs a live answer. For online, I validate input with a typed schema, load the model once, expose health and readiness endpoints, and version the route and the model."

Do not claim that FastAPI makes a model fast. It only handles HTTP.

## Likely interview questions

- **When batch instead of online?** When no user waits and the data changes slowly; batch is cheaper and easier to monitor and rerun.
- **How do you protect the service from bad input?** Validate at the boundary with a typed schema and return a clear 4xx error.
- **How do you roll out a new model safely?** Deploy it next to the old version, send a small share of traffic, compare, then switch.

## See also

- [Input validation and data contracts](#/kb/prod-input-validation)
- [Health checks](#/kb/prod-health-checks)
- [Training-serving skew](#/kb/prod-train-serve-skew)
