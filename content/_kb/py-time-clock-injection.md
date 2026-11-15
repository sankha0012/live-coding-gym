---
title: "Clocks: time.monotonic and injecting a clock or sleep"
summary: Measure elapsed time with time.monotonic, and pass clock and sleep in as parameters so tests can fake them.
tags: [python, time, testing]
---
```python
import time

def wait_until(ready, timeout=5.0, interval=0.5,
               clock=time.monotonic, sleep=time.sleep):   # real ones by default
    deadline = clock() + timeout
    while clock() < deadline:
        if ready():
            return True
        sleep(interval)
    return False
```

- `time.monotonic()` never goes backwards. Use it for durations, timeouts and TTLs.
- `time.time()` is the wall clock. It can jump when the system clock is corrected.
- Pass the function itself (`clock=time.monotonic`), not a call (`clock=time.monotonic()`).

<!-- more -->

## Details

Measuring how long something takes:

```python
start = time.monotonic()
do_work()
elapsed = time.monotonic() - start     # seconds as a float
```

The value of `monotonic()` on its own means nothing. Only the difference between two readings is useful. `time.perf_counter()` is the same idea with the highest resolution, for benchmarks.

Code that calls `time.monotonic()` and `time.sleep()` directly is slow and awkward to test. If the clock and the sleep function are parameters, a test can hand in fakes that it controls. No real waiting happens:

```python
class FakeClock:
    def __init__(self):
        self.now = 0.0
    def __call__(self):            # used as clock()
        return self.now
    def sleep(self, seconds):      # used as sleep(seconds)
        self.now += seconds

fake = FakeClock()
wait_until(lambda: False, timeout=2.0, clock=fake, sleep=fake.sleep)   # False, instantly
fake.now                           # 2.0   four fake sleeps of 0.5
```

Sometimes a fake sleep only needs to record what was asked. A list's `append` method is enough:

```python
slept = []
retry(flaky, attempts=3, delay=1.0, sleep=slept.append)
slept                              # [1.0, 2.0]   the backoff delays, no real waiting
```

For a class, take the clock in `__init__` and store it:

```python
class TTLCache:
    def __init__(self, ttl, clock=time.monotonic):
        self.ttl = ttl
        self.clock = clock         # later: expires_at = self.clock() + self.ttl
```

In a test a lambda over a mutable value works as a clock: `now = [100.0]`, `clock=lambda: now[0]`, then `now[0] += 10` to move time forward.

The same idea applies to dates: accept `now` or a `today` function as a parameter instead of calling `datetime.now()` deep inside the logic.

## Common mistakes

- Writing `clock=time.monotonic()` as a default. The time is then frozen at import.
- Using `time.time()` for a timeout. A clock adjustment can make it fire early or never.
- Injecting the clock but still calling `time.sleep` directly somewhere in the loop.
- Comparing fake times that were built by adding many small floats with `==`. Use `>=` or `pytest.approx`.
- Calling real `time.sleep` in tests, which makes the suite slow and flaky.

## See also

- [Fakes, fake clocks and monkeypatch](#/kb/test-fakes-monkeypatch)
- [Retries with backoff](#/kb/prod-retry-backoff)
- [Caches with a TTL](#/kb/prod-ttl-cache)
- [Timeouts and deadlines](#/kb/prod-timeouts-deadlines)
- Official docs: https://docs.python.org/3/library/time.html
