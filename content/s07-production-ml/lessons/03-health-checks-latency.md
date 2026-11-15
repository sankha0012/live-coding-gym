# Health checks and latency percentiles

## What it is

A health check is an endpoint the platform calls to decide what to do with an instance. Liveness answers "is the process running", and the platform restarts it if not. Readiness answers "can it serve right now", meaning the model is loaded and dependencies respond, and the load balancer routes traffic only to ready instances. Latency percentiles describe response time honestly: p50 is the typical request, p95 and p99 are the tail. See [health checks](#/kb/prod-health-checks) and [percentiles](#/kb/prod-monitoring-percentiles).

## How it breaks in production

A single check that always returns "ok" hides a service that is up but has no model loaded, so traffic goes to an instance that fails every request. The opposite mistake is a liveness check that calls the database: when the database is slow, the platform restarts every healthy instance and turns a small problem into an outage. Averages hide tail pain. If most requests take 30 ms and one in a hundred takes two seconds, the mean looks fine while real users wait. Percentiles also break in code: an empty list has no percentile, and a p99 computed from ten samples is just the maximum.

## The defence in code

```python
import math

def percentile(values, p):
    if not values:
        raise ValueError("no values")
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))      # nearest rank, 1-based
    return ordered[max(rank, 1) - 1]

def liveness() -> dict:
    return {"status": "alive"}                    # no dependencies on purpose

def readiness(model, feature_store_ok: bool) -> tuple[int, dict]:
    problems = []
    if model is None:
        problems.append("model not loaded")
    if not feature_store_ok:
        problems.append("feature store unreachable")
    return (503, {"problems": problems}) if problems else (200, {"status": "ready"})

latencies = [20, 22, 25, 30, 31, 35, 40, 45, 300, 2000]
print(percentile(latencies, 50), percentile(latencies, 95), percentile(latencies, 99))
print(sum(latencies) / len(latencies))
print(readiness(None, True))
print(readiness(object(), True))
```

The mean is 254.8 ms and describes nobody; p50 is 31 ms and p99 is 2000 ms. Liveness has no dependencies. Readiness fails with 503 and a reason, so the router stops sending traffic and a human can see why.

## What to say in the interview

"I expose two endpoints. Liveness only says the process is up, and readiness says the model is loaded and the dependencies answer, so the router sends traffic only to instances that can serve. I report p50, p95 and p99 latency rather than the mean, because the tail is what users feel, and I make sure I have enough samples for the p99 to mean something. I alert on p99 and error rate."
