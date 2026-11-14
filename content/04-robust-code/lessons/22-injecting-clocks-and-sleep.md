# Injecting clocks and sleep

## The problem it solves

Code that reads the system clock or calls `time.sleep` is hard to test. A retry loop with a real sleep of two seconds makes the test slow. A check like "is this older than one hour" gives a different answer at a different time of day. A rate limiter that depends on the real clock gives flaky tests.

The fix is small: do not call the clock yourself. Take it as a parameter. In production you pass the real one. In tests you pass a fake one that you control.

## The smallest runnable example

```python
import time


def retry(fn, attempts, delay, sleep=time.sleep):
    for i in range(attempts):
        try:
            return fn()
        except ConnectionError:
            if i == attempts - 1:
                raise
            sleep(delay * 2 ** i)     # wait 1x, 2x, 4x ...


class FakeClock:
    def __init__(self, start=0.0):
        self.now = start

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds           # time moves forward, instantly


calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("down")
    return "ok"


clock = FakeClock()
assert retry(flaky, attempts=5, delay=1.0, sleep=clock.sleep) == "ok"
assert clock.now == 3.0               # slept 1 + 2 seconds, in zero real time
print("slept", clock.now, "seconds (fake)")
```

The function has two arguments with defaults that point to the real thing: `sleep=time.sleep`. Callers who do not care never notice. The test passes `clock.sleep`, runs instantly, and can assert exactly how long the code would have waited.

## Injecting a clock for "now"

The same idea works for reading the time. Pass a callable, not a value, when the code needs to ask many times.

```python
import time


def run_until(deadline_s, step, clock=time.monotonic):
    start = clock()
    done = 0
    while clock() - start < deadline_s:
        step()
        done += 1
    return done


ticks = iter([0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
n = run_until(3.0, lambda: None, clock=lambda: next(ticks))
print(n)
```

Use `time.monotonic` for durations and deadlines. It never goes backwards when someone changes the system time. Use a timezone-aware UTC `datetime` only when you need a calendar date.

If the function needs "today" or "now" as a value, passing the value itself is even simpler: `def is_stale(ts, now): return now - ts > 3600`. The test then passes any `now` it likes.

## Three traps people hit

1. **Default argument evaluated too early.** Writing `now=datetime.now()` as a default freezes the time when the function is defined, not when it is called. Use `now=None` and read the clock inside, or take a callable.
2. **Faking the clock but not the sleep.** If your fake clock is separate from `sleep`, the loop can wait forever, because sleeping does not move the fake time. Make the fake `sleep` advance the fake clock, as `FakeClock` above does.
3. **Patching globals instead of passing arguments.** `unittest.mock.patch("time.sleep")` works but hides the dependency and breaks when the module imports `sleep` by another name. A parameter is visible in the signature, and the reviewer can see the code is testable.

## Why interviewers like it

When a task says "retry with backoff" or "rate limit", the hidden checks cannot wait real seconds. If your function accepts `sleep` and `clock`, you have solved the testing problem before anyone asks. It also shows that you separate logic from side effects, which is the main idea behind code that survives production.

## Say it like this

"I do not read the clock or call sleep directly. I take them as parameters, with the real functions as defaults. In production nothing changes. In tests I pass a fake clock whose sleep advances the fake time, so a retry with exponential backoff runs instantly and I can assert the exact total wait. I use the monotonic clock for deadlines so a system time change cannot break them. The cost is one extra argument, and the gain is fast, deterministic tests."
