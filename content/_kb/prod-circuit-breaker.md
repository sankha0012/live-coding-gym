---
title: Circuit breaker
summary: After repeated failures stop calling a broken dependency for a cooldown, then let one trial call through.
tags: [production, reliability]
---
```python
class Breaker:
    def __init__(self, max_failures, cooldown, clock):
        self.max_failures, self.cooldown, self.clock = max_failures, cooldown, clock
        self.failures, self.opened_at = 0, None
    def allow(self):                    # False while open and still cooling down
        return self.opened_at is None or self.clock() - self.opened_at >= self.cooldown

    def record(self, ok):
        if ok:
            self.failures, self.opened_at = 0, None    # success closes it
            return
        self.failures += 1
        if self.failures >= self.max_failures:
            self.opened_at = self.clock()              # open, or re-open after a failed trial
```

- Use it around a dependency that can be down for minutes: a model server, a feature store, an API.
- Key rule: three states. Closed (calls pass), open (fail fast), half-open (one trial after the cooldown).
- Say: "Retries handle a blip. The breaker handles an outage, and gives the dependency room to recover."

<!-- more -->

## Details

The caller wraps each call:

```python
def guarded(breaker, fn, fallback):
    if not breaker.allow():
        return fallback                 # fail fast: fn is not called
    try:
        result = fn()
    except Exception:
        breaker.record(False)
        return fallback
    breaker.record(True)
    return result
```

A run with a fake clock:

```python
t = [0.0]
b = Breaker(max_failures=2, cooldown=30, clock=lambda: t[0])
b.record(False)
b.record(False)
b.allow()            # False  open: two failures in a row
t[0] = 30.0
b.allow()            # True   cooldown over: half-open, try once
b.record(False)
b.allow()            # False  trial failed: open again, cooldown restarts at t=30
```

The failure count is not reset when the breaker opens. So one failed trial is already at the limit and opens it again with a new `opened_at`.

Failing fast matters because a slow, failing call holds a thread and a connection. Many of them take the caller down too.

This sketch lets every caller through once the cooldown ends. A strict half-open state allows one trial at a time, which needs a flag and, with threads, a lock.

## Common mistakes

- Not resetting the failure count on success, so scattered failures over a day open the breaker.
- Using `>` instead of `>=` for the cooldown or the failure limit: an off-by-one at the boundary.
- Restarting the cooldown on every rejected call, so a busy breaker never tries again.
- Calling the real clock inside the class, which makes the test sleep.
- Counting bad input (a `ValueError` from the caller) as a dependency failure.

## See also

- [Retries with backoff](#/kb/prod-retry-backoff)
- [Fallbacks and fallback chains](#/kb/prod-fallbacks)
- [Health checks](#/kb/prod-health-checks)
- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
