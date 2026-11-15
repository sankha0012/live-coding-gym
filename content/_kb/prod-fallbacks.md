---
title: Fallbacks and fallback chains
summary: When the best source fails or returns garbage, try the next simpler one and record which one answered.
tags: [production, reliability]
---
```python
import math

def first_good(sources, default):
    for name, fn in sources:                # ordered best to worst
        try:
            value = fn()
        except Exception:
            continue                        # in real code: log name and error
        if value is not None and not math.isnan(value):
            return value, name              # say which source answered
    return default, "default"
```

- Use it when an answer is required even if the model, cache or feature store is down.
- Key rule: a bad value (None, NaN, out of range) counts as a failure, the same as an exception.
- Say: "I return the source name with the value, so the fallback rate can be monitored."

<!-- more -->

## Details

A typical chain for a prediction: the live model, then the last cached score, then a simple rule, then a safe constant. Each step is cheaper and more reliable than the one before, and less accurate.

```python
def model():
    raise TimeoutError("slow")

sources = [("model", model), ("cache", lambda: float("nan")), ("rule", lambda: 0.3)]
first_good(sources, default=0.0)      # (0.3, 'rule')
first_good([], default=0.0)           # (0.0, 'default')
```

The model raised, the cache returned NaN, so the rule answered.

Design points:

- **The last step cannot fail.** It is a constant or pure arithmetic, with no I/O.
- **Validate, do not only catch.** A model that returns NaN or 7.3 for a probability did not raise, but its answer is unusable.
- **Make it visible.** Count how often each source answers. A fallback rate that climbs from 1% to 40% is an incident, even though no request failed.
- **Choose the default for the business.** For fraud, "send to manual review" may be safer than "approve".
- **Know when not to fall back.** For a payment amount there is no safe guess. Fail loudly.

A fallback is often combined with a timeout (stop waiting for the model) and a circuit breaker (stop calling it for a while).

## Common mistakes

- Catching the exception and continuing with no log and no counter, so nobody knows the model is down.
- Treating only exceptions as failures and passing NaN or None downstream.
- Using `except:` or `except BaseException`, which also swallows `KeyboardInterrupt`.
- A fallback that calls the same broken dependency.
- Returning a value with no hint that it is a fallback, so it is later used as a real prediction.

## See also

- [Timeouts and deadlines](#/kb/prod-timeouts-deadlines)
- [Circuit breaker](#/kb/prod-circuit-breaker)
- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
- [Exceptions: try, except, raise, custom errors](#/kb/py-exceptions)
