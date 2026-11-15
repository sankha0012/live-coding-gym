# Stale models and stale data

## What it is

A stale model is one that has not been retrained for longer than it should have been. Stale data is the sibling problem: the model is fine, but the feed that supplies its inputs stopped updating. In both cases the system keeps answering, with confidence, from an outdated picture of the world.

## How it breaks in production

The retrain job fails silently, for example after a credentials change, and the model in production is now weeks old. Or an upstream table stops refreshing and the "last 7 days of orders" feature quietly turns into "the 7 days before the outage". Neither case throws an exception. The service is up, latency is normal, and quality drifts down. People notice only when a business metric drops. The defence is not smarter modelling but metadata: every model should carry its training time, and every feed should expose the timestamp of its newest record. See [health checks](#/kb/prod-health-checks) and [fallbacks](#/kb/prod-fallbacks).

## The defence in code

Compare ages to limits and decide what to do when they are exceeded. Pass the clock in as a parameter so the function is deterministic and testable; calling `datetime.now()` inside makes tests flaky. See [determinism](#/kb/prod-determinism).

```python
from datetime import datetime, timedelta, timezone

def freshness(now, trained_at, newest_event, max_model_age, max_data_lag):
    problems = []
    if now - trained_at > max_model_age:
        problems.append("stale_model")
    if now - newest_event > max_data_lag:
        problems.append("stale_data")
    return problems

now = datetime(2026, 11, 15, 12, 0, tzinfo=timezone.utc)
ok = freshness(now, now - timedelta(days=3), now - timedelta(minutes=5),
               timedelta(days=14), timedelta(hours=1))
old = freshness(now, now - timedelta(days=30), now - timedelta(hours=6),
                timedelta(days=14), timedelta(hours=1))
assert ok == []
assert old == ["stale_model", "stale_data"]
print(old)
```

Note that the datetimes are timezone-aware. Subtracting an aware datetime from a naive one raises an error, which is better than a silent hour-sized mistake. What the service does with the result is a decision: a stale model might still serve with an alarm, while stale data feeding a payment decision should fall back to a rule or refuse.

## What to say in the interview

"I would store the training time with the model and expose the newest event time of each feed, then check both ages against limits on every health check. The function takes the current time as an argument so I can test it without waiting. When something is stale I alarm, and then either serve a fallback rule or refuse, depending on whether a wrong answer or no answer is more expensive."
