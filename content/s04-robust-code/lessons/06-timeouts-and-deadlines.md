# Timeouts and deadlines

## What it is

A timeout limits how long one call may take. A deadline limits how long a whole operation may take, including every retry and every wait between them. You set the deadline once, as a point in time on the monotonic clock, and each step asks how much time is left. See [Timeouts and deadlines](#/kb/prod-timeouts-deadlines) and [Fallbacks](#/kb/prod-fallbacks).

## How it breaks in production

Many network libraries wait forever unless told otherwise: `requests.get(url)` has no timeout by default, so one stuck dependency freezes a worker, then all workers, then the service. The second failure is timeouts that add up. Three attempts with a 10 second timeout each, plus backoff, is over 30 seconds, while the caller gave up after 5. The work continues for nobody. Third, a timeout on a thread does not stop the thread: `future.result(timeout=1)` raises in the caller, but the worker keeps running. Last, measuring with `time.time()` is wrong because the wall clock can jump; use `time.monotonic()`.

## The defence in code

```python
import time


class DeadlineExceeded(Exception):
    pass


def call_with_deadline(fn, budget, attempts=3, clock=time.monotonic, sleep=time.sleep):
    deadline = clock() + budget
    for i in range(attempts):
        remaining = deadline - clock()
        if remaining <= 0:
            raise DeadlineExceeded("no time left")
        try:
            return fn(timeout=remaining)          # each call gets only what is left
        except TimeoutError:
            if i == attempts - 1:
                raise
            sleep(min(0.5 * 2 ** i, max(0.0, deadline - clock())))


class Fake:
    def __init__(self):
        self.now = 0.0

    def clock(self):
        return self.now

    def sleep(self, s):
        self.now += s


f = Fake()


def slow(timeout):
    f.now += timeout                  # the call uses all the time it is given
    raise TimeoutError


try:
    call_with_deadline(slow, budget=5.0, clock=f.clock, sleep=f.sleep)
except (TimeoutError, DeadlineExceeded) as e:
    print(type(e).__name__, "after", f.now, "fake seconds")
assert f.now <= 5.0                   # never exceeds the budget
```

The deadline is computed once. Every attempt receives the remaining time as its timeout, and the sleep is cut to what remains, so the total cannot exceed the budget. With a fake clock the test finishes instantly and checks that bound exactly. When the deadline is hit, fall back to a safe default or fail clearly, and count it.

## What to say in the interview

"I give every external call a timeout, because most clients wait forever by default. For an operation with retries I set one deadline on the monotonic clock and pass each attempt the remaining time, so the total never exceeds the caller's budget. A thread timeout does not kill the thread, so I keep the work cancellable or idempotent. On timeout I fall back or fail clearly, and I count it."
