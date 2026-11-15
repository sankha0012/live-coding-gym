---
title: Timeouts and deadlines
summary: Give every call a time limit, and give a whole request one deadline that all its steps share.
tags: [production, reliability]
---
```python
def call_all(steps, budget, clock):
    deadline = clock() + budget             # one absolute deadline for the request
    out = []
    for step in steps:
        remaining = deadline - clock()
        if remaining <= 0:
            raise TimeoutError(f"deadline passed after {len(out)} steps")
        out.append(step(timeout=remaining)) # each call gets what is left
    return out
```

- Use it on every network call, queue read, lock and batch loop. No call should wait forever.
- Key rule: a timeout is per call, a deadline is one fixed point in time for the whole job.
- Say: "I compute the deadline once and pass the remaining budget down, so three slow steps cannot each use the full limit."

<!-- more -->

## Details

A **timeout** is a duration: "wait at most 2 seconds for this call". A **deadline** is a moment: "the answer is useless after t = 105". With only per-call timeouts, five calls of 2 seconds can take 10 seconds. With a deadline, each call receives `deadline - now`.

```python
t = [0.0]

def step(timeout):
    t[0] += 0.4                 # pretend the call took 0.4 s
    return round(timeout, 1)

call_all([step, step, step], budget=1.0, clock=lambda: t[0])   # [1.0, 0.6, 0.2]
```

A fourth step would raise `TimeoutError`, because 1.2 seconds have passed.

Check the clock **before** starting each piece of work. Work that has started normally runs to its end: Python cannot safely kill a running thread. A timeout on `future.result(timeout=...)` stops the waiting, not the work.

Use `time.monotonic` for durations. `time.time` can jump when the system clock is corrected.

When the deadline passes you have two honest choices: raise, or return the partial result together with what was not done. Say which one you chose.

## Common mistakes

- No timeout at all on a network call. Many libraries default to waiting forever.
- Restarting the full timeout for each step or each retry, so the total has no limit.
- Measuring with wall-clock time instead of a monotonic clock.
- Using `<` in one place and `<=` in another for the boundary. Decide once what "exactly at the deadline" means.
- Dropping unfinished items silently instead of returning or logging them.

## See also

- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
- [Retries with backoff](#/kb/prod-retry-backoff)
- [Fallbacks and fallback chains](#/kb/prod-fallbacks)
