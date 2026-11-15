---
title: Retries with backoff
summary: Call again after a transient failure, waiting longer each time, with a hard limit on attempts.
tags: [production, reliability]
---
```python
def retry(fn, tries, base, sleep, retryable=(ConnectionError, TimeoutError)):
    if tries < 1:
        raise ValueError("tries must be at least 1")
    for attempt in range(tries):
        try:
            return fn()
        except retryable:
            if attempt == tries - 1:
                raise                       # out of tries: surface the last error
            sleep(base * 2 ** attempt)      # base, 2*base, 4*base ...
```

- Use it for transient failures: network errors, timeouts, HTTP 429 and 503.
- Key rule: bounded attempts, growing waits, retry only errors that can go away, never sleep after the last failure.
- Say: "I inject sleep so the test runs instantly and I can assert the exact waits."

<!-- more -->

## Details

```python
calls, waits = [], []

def flaky():
    calls.append(1)
    if len(calls) < 3:
        raise ConnectionError("down")
    return "ok"

retry(flaky, tries=4, base=0.5, sleep=waits.append)   # 'ok'
waits                                                  # [0.5, 1.0]
```

The fake `sleep` is `waits.append`. It records each delay and returns at once.

**Classify errors.** A `ValueError` from bad input will fail the same way every time. Let it pass through. Only the `retryable` types are caught.

**Cap the delay.** Exponential waits grow fast. Use `min(cap, base * 2 ** attempt)`.

**Add jitter.** When many clients fail together, they also retry together. Spread them with a random delay from an injected generator:

```python
import random

def delay(attempt, base, cap, rng):
    return rng.uniform(0, min(cap, base * 2 ** attempt))   # "full jitter"

0 <= delay(3, 0.5, 2.0, random.Random(0)) <= 2.0           # True
```

**Retries multiply load.** Three layers that each retry three times make 27 calls. Retry at one layer, and combine retries with a deadline for the whole request.

## Common mistakes

- Catching `Exception` and retrying programming errors and bad input.
- Sleeping after the final failure, which only delays the error.
- Calling `time.sleep` directly, so tests are slow and the waits cannot be checked.
- Retrying an operation that is not idempotent, such as a charge, and doing it twice.
- Swallowing the last error and returning `None` instead of re-raising.

## See also

- [Idempotency and idempotency keys](#/kb/prod-idempotency)
- [Timeouts and deadlines](#/kb/prod-timeouts-deadlines)
- [Circuit breaker](#/kb/prod-circuit-breaker)
- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
