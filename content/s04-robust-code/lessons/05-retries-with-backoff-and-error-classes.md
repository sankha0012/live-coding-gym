# Retries with backoff and error classes

## What it is

A retry calls an operation again after it failed. Backoff makes each wait longer than the last, usually doubling, so a struggling service gets room to recover. Error classes are the decision about which failures deserve a retry at all: transient ones, such as timeouts, connection resets and HTTP 429 or 503, can succeed later; permanent ones, such as a 400 or a bug in your code, cannot. See [Retry with backoff](#/kb/prod-retry-backoff).

## How it breaks in production

Retrying everything wastes time and hides bugs: a `ValueError` retried five times is still a `ValueError`, only slower. Retrying with no wait, or a fixed wait, makes an outage worse because every client hammers the failing service. Without a cap on attempts or on the delay, the loop either never ends or waits minutes. Without jitter, thousands of clients that failed together retry together. And a retry that swallows the final error and returns `None` turns a loud failure into silent bad data. Retrying a non-idempotent call, such as a payment, can also run it twice, which is why retries and [idempotency keys](#/kb/prod-idempotency) go together.

## The defence in code

```python
import random


class TransientError(Exception):
    pass


def call_with_retry(fn, attempts=4, base=1.0, cap=8.0, sleep=lambda s: None, rng=None):
    rng = rng or random.Random(0)
    for i in range(attempts):
        try:
            return fn()
        except TransientError:                 # only the transient class
            if i == attempts - 1:
                raise                          # out of attempts: the caller sees it
            delay = min(cap, base * 2 ** i)
            sleep(delay * (0.5 + rng.random() / 2))   # jitter in [50%, 100%]


waits, state = [], {"n": 0}


def flaky():
    state["n"] += 1
    if state["n"] < 3:
        raise TransientError("503")
    return "ok"


assert call_with_retry(flaky, sleep=waits.append) == "ok"
assert len(waits) == 2 and 0.5 <= waits[0] <= 1.0 and 1.0 <= waits[1] <= 2.0

try:
    call_with_retry(lambda: 1 / 0, sleep=waits.append)
except ZeroDivisionError:
    print("bug was not retried")
```

Only `TransientError` is caught, so a bug fails at once. The delay is `base * 2 ** i`, capped, then reduced by random jitter. The random generator and the sleep are parameters, so the test is deterministic and instant. The last attempt re-raises.

## What to say in the interview

"I retry only errors I have classified as transient, with exponential backoff, a cap on the delay, jitter and a maximum number of attempts. Permanent errors and bugs fail immediately. When I run out of attempts I re-raise the last error instead of returning a fake result. Sleep and the random generator are parameters, so the test is instant. And I only retry calls that are safe to repeat."
