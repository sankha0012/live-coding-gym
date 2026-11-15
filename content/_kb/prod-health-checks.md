---
title: Health checks
summary: A cheap function that runs named checks and reports ok or unhealthy with the reason for each.
tags: [production, monitoring]
---
```python
def health(checks):
    """checks: name -> function that returns normally or raises."""
    results = {}
    for name, check in checks.items():
        try:
            check()
            results[name] = "ok"
        except Exception as e:
            results[name] = f"fail: {type(e).__name__}"
    status = "ok" if all(v == "ok" for v in results.values()) else "unhealthy"
    return {"status": status, "checks": results}
```

- Use it so a load balancer or orchestrator can decide to route traffic to, or restart, an instance.
- Key rule: run every check, never raise, and report each result by name.
- Say: "Liveness asks if the process is stuck. Readiness asks if it can serve a request right now."

<!-- more -->

## Details

```python
def db():
    raise ConnectionError("refused")

health({"model_loaded": lambda: None, "db": db})
# {'status': 'unhealthy', 'checks': {'model_loaded': 'ok', 'db': 'fail: ConnectionError'}}
health({})["status"]     # 'ok'   no checks: decide if that should really be ok
```

**Liveness and readiness.** A failed liveness check restarts the process, so it must test only the process itself. A failed readiness check removes the instance from traffic until it recovers. If liveness depends on the database, a database outage restarts every instance for nothing.

**Critical and optional.** Not every dependency is required. A common third status is `degraded`: an optional check failed (the cache is down), but requests still work through a fallback.

**Useful checks for a model service:**

- The model is loaded and its version is the expected one.
- A fixed smoke input gives a finite score in range.
- The feature store answers within a short timeout.
- Freshness: the model or the last data update is not older than a limit. Pass `now` in so the check is testable.

```python
def fresh(updated_at, now, max_age):
    if now - updated_at > max_age:
        raise RuntimeError("stale")

health({"data_fresh": lambda: fresh(updated_at=100, now=4000, max_age=3600)})["status"]   # 'unhealthy'
```

**Keep it cheap.** The endpoint is called every few seconds. Give each check a timeout, and cache slow results for a short time.

## Common mistakes

- Returning "ok" as long as the process is up, even when the model failed to load.
- Stopping at the first failed check, so the report hides the others.
- Letting an exception escape, so the health endpoint itself returns an error with no detail.
- A check with no timeout that hangs the health endpoint.
- Putting secrets or full stack traces in the response.

## See also

- [Monitoring and latency percentiles](#/kb/prod-monitoring-percentiles)
- [Circuit breaker](#/kb/prod-circuit-breaker)
- [Timeouts and deadlines](#/kb/prod-timeouts-deadlines)
