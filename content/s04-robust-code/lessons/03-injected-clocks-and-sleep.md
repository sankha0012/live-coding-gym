# Injected clocks and sleep

## What it is

Injecting a clock means your function does not call `time.time()`, `datetime.now()` or `time.sleep()` itself. It receives them as parameters, with the real ones as defaults. In production nothing changes. In a test you pass a fake whose time you control. See [Clock injection](#/kb/py-time-clock-injection) and [Dates and datetimes in Python](#/kb/py-datetime).

## How it breaks in production

Code that reads the real clock cannot be checked exactly. A cache that expires after 60 seconds, a rate limiter, a "stale if older than one hour" rule and a retry loop with a two-second sleep all behave differently at different moments. The tests either sleep for real, which is slow, or depend on the time of day, so they fail only at midnight or at month end. A related trap is `def f(now=datetime.now())`: the default is evaluated once, when the function is defined, so every call sees the same frozen time. A third is using the wall clock for durations: it can jump when the system clock is corrected, so a timeout can fire early or never. Use `time.monotonic()` for durations and aware UTC datetimes for calendar dates.

## The defence in code

```python
import time


class FakeClock:
    def __init__(self, start=0.0):
        self.now = start

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds        # sleeping moves the fake time, instantly


def retry(fn, attempts, delay, sleep=time.sleep):
    for i in range(attempts):
        try:
            return fn()
        except ConnectionError:
            if i == attempts - 1:
                raise
            sleep(delay * 2 ** i)


def is_stale(ts, now, max_age=3600):
    return now - ts > max_age       # "now" is a plain argument


calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("down")
    return "ok"


clock = FakeClock()
assert retry(flaky, attempts=5, delay=1.0, sleep=clock.sleep) == "ok"
assert clock.monotonic() == 3.0     # waited 1 + 2 seconds, in zero real time
assert is_stale(0, now=3601) and not is_stale(0, now=3600)
print("fake seconds waited:", clock.monotonic())
```

The retry waits one and then two seconds, and the test asserts the exact total without sleeping. The fake `sleep` advances the fake clock; if it did not, any loop that waits for time to pass would spin forever. The last assert pins the boundary: exactly one hour old is not stale.

## What to say in the interview

"I never read the clock or call sleep directly. I pass them in as parameters, with the real functions as defaults, so production is unchanged. In tests I pass a fake whose sleep advances the fake time, which lets me run a backoff in zero seconds and assert the exact waits. For durations I use the monotonic clock so a system time change cannot break a deadline."
