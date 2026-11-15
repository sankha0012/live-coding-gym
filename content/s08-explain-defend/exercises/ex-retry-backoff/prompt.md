Read this listing. It runs on Python 3.12.

```python
import random
import time


class TransientError(Exception):
    pass


def retry(fn, attempts=4, base=0.5, cap=8.0, sleep=time.sleep, rng=None):
    """Call fn(); on TransientError wait with exponential backoff and jitter."""
    rng = rng or random.Random()
    for attempt in range(attempts):
        try:
            return fn()
        except TransientError:
            if attempt == attempts - 1:
                raise
            delay = min(cap, base * 2 ** attempt)
            sleep(rng.uniform(0, delay))


if __name__ == "__main__":
    calls = {"n": 0}
    waits = []

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TransientError("503")
        return "ok"

    print(retry(flaky, sleep=waits.append, rng=random.Random(7)))
    print(calls["n"], [round(w, 3) for w in waits])

    def always_down():
        raise TransientError("down")

    try:
        retry(always_down, attempts=3, sleep=waits.append, rng=random.Random(7))
    except TransientError as exc:
        print("gave up:", exc)
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
