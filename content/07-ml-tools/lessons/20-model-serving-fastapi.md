# Model serving with FastAPI

## What problem it solves

A trained model is a file. Other systems cannot use a file. They need to send a request and get a prediction back. Serving turns the model into a service with a stable contract: this input shape in, this output shape out.

There are two main modes.

- **Online serving.** One request, one prediction, answered in milliseconds. Use it when a user waits: a fraud check at payment time, a delivery time estimate in an app.
- **Batch serving.** A job scores many rows on a schedule and writes the results to a table. Use it when nobody waits: a nightly list of customers likely to churn.

Batch is simpler, cheaper and easier to test. Choose online only when the answer must reflect fresh data or a live user action.

FastAPI is a Python web framework. It is popular for ML serving because it validates requests with pydantic types and writes API docs for you.

## Where it sits in an ML pipeline

It is the last step before the consumer. Training produces a model artifact. The serving code loads that artifact once at startup, then handles requests. In front of it sits a load balancer or gateway. Behind it sit the feature sources. In a container (see the Docker lesson) it is the thing that gets deployed.

## A minimal real example

This was run with FastAPI's test client and a small scikit-learn model saved to `model.joblib`. A valid request returned 200 with a prediction. A request with `distance_km: -1` returned 422 with the message "Input should be greater than 0". `/health` returned `{"status": "ok"}`.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

app = FastAPI()
model = joblib.load("model.joblib")   # load once, not per request


class Order(BaseModel):
    distance_km: float = Field(gt=0)
    items: int = Field(ge=1)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/predict")
def predict(order: Order):
    pred = model.predict([[order.distance_km, order.items]])[0]
    return {"minutes": float(pred), "model_version": "2026-11-01"}
```

Bad input, such as a negative distance, is rejected with a 422 error before your code runs. That is the main value of the type model.

The same idea works without any framework. This part runs on plain Python: validate first, then predict, and fail loudly with a clear message.

```python
def validate(payload: dict) -> dict:
    distance = payload.get("distance_km")
    items = payload.get("items")
    if not isinstance(distance, (int, float)) or distance <= 0:
        raise ValueError("distance_km must be a positive number")
    if not isinstance(items, int) or items < 1:
        raise ValueError("items must be an integer >= 1")
    return {"distance_km": float(distance), "items": items}


print(validate({"distance_km": 3, "items": 2}))
try:
    validate({"distance_km": -1, "items": 2})
except ValueError as e:
    print("rejected:", e)
```

## Points that matter

- **Request validation.** Never trust the caller. Check types, ranges and required fields at the boundary. Reject with a clear 4xx error, not a stack trace.
- **Health checks.** A liveness endpoint says the process is up. A readiness endpoint says the model is loaded and the service can take traffic. Orchestrators use them to restart or route.
- **Latency.** Load the model at startup. Keep preprocessing in the same code path as training. Measure p50 and p99, not only the average, because a few slow requests hurt users most.
- **Versioned endpoints.** Put a version in the path (`/v1/predict`) and return the model version in the response. Then you can ship `/v2` without breaking old clients, and you can trace any prediction to a model.

## Three traps

1. Loading the model inside the request handler. It makes every call slow.
2. Different preprocessing in serving than in training. Predictions quietly go wrong.
3. No input checks, so one malformed request crashes the worker or returns a silent wrong answer.

## What to say in an interview

Say: "I would choose batch unless the use case needs a live answer. For online, I would validate input with a typed schema, load the model once, expose health and readiness endpoints, and version the route and the model."

Do NOT claim:

- That FastAPI makes a model fast. It only handles HTTP. Latency comes from the model, the features and the infrastructure.
- That you have run it at scale, unless you have.
- That online is better than batch. It is only more costly and more complex.

## Three likely questions

**1. When would you use batch instead of online?**
When no user waits for the answer and the data changes slowly. Batch is cheaper, simpler and easier to monitor and rerun.

**2. How do you protect the service from bad input?**
Validate at the boundary with a typed schema. Check types, ranges and required fields. Return a clear 4xx error. Log the rejected request so I can see data problems early.

**3. How do you roll out a new model safely?**
Version the model and the route. Deploy the new version next to the old one. Send a small share of traffic, compare metrics, then switch over. Keep the old version ready for a fast rollback.
