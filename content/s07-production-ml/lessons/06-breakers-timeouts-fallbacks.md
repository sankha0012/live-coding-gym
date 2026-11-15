# Circuit breakers, timeouts and fallbacks

## What it is

Three tools that stop one failing dependency from taking down the caller. A timeout bounds how long you wait. A fallback is the answer you return when the real one is unavailable, such as the last known score or a global average. A circuit breaker counts failures, and after a threshold it opens: for a cool-down period it fails fast without calling the dependency at all, then lets one trial call through to see if it has recovered. See [circuit breaker](#/kb/prod-circuit-breaker), [timeouts](#/kb/prod-timeouts-deadlines) and [fallbacks](#/kb/prod-fallbacks).

## How it breaks in production

A call with no timeout waits forever, so threads pile up behind one slow model server until the whole service is stuck. A retry loop with no breaker makes it worse: every request hammers a dependency that is already struggling. A breaker that never closes again leaves you on the fallback long after the dependency recovered, and one that closes too eagerly flaps. A fallback is also dangerous when invisible. If you quietly return the average for everyone, the service looks healthy while quality collapses, so the fallback rate must be counted and alerted. Finally, a fallback must be safe for the use case: a default delivery time is fine, a default fraud score of zero is not.

## The defence in code

```python
class Breaker:
    def __init__(self, threshold: int, cooldown: float, clock):
        self.threshold, self.cooldown, self.clock = threshold, cooldown, clock
        self.failures, self.opened_at = 0, None

    def call(self, fn, fallback):
        if self.opened_at is not None:
            if self.clock() - self.opened_at < self.cooldown:
                return fallback()                    # open: fail fast
            self.opened_at = None                    # cool-down over: allow a trial
        try:
            result = fn()
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold:
                self.opened_at = self.clock()
            return fallback()
        self.failures = 0
        return result

def broken():
    raise TimeoutError("model server timed out")

t = [0.0]
b = Breaker(threshold=2, cooldown=30, clock=lambda: t[0])
print([b.call(broken, lambda: "fallback") for _ in range(4)])
t[0] = 31.0
print(b.call(lambda: "model answer", lambda: "fallback"))   # trial succeeds, breaker closes
```

After two failures the breaker opens and later calls skip the dependency. After the cool-down one trial succeeds and service resumes. In real code `fn` carries its own timeout.

## What to say in the interview

"Every remote call gets a timeout, derived from the overall deadline of the request. I retry only idempotent calls, with backoff and a limit. A circuit breaker stops me from hammering a failing dependency and gives it time to recover. The fallback is chosen for safety in this use case, and I log and count it, so a degraded service is visible and not silently wrong."
