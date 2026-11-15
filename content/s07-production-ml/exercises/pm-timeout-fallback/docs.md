# predict_with_fallback: reference

## Contract

`predict_with_fallback(model, x, fallback, deadline_s, clock) -> tuple` calls `model(x)` once and returns `(value, path)`.

- `clock()` returns the current time in seconds. Read it before and after the call. Never read the real clock.
- The call returned normally and took at most `deadline_s` seconds (exactly equal is on time): return `(model_result, "model")`.
- The call returned normally but took more than `deadline_s`: the result is discarded and the return is `(fallback, "timeout")`.
- `model(x)` raised any `Exception`: return `(fallback, "error")`, with no retry. The exception does not escape. A call that is both slow and raising is `"error"`.
- `model` is called exactly once in every case.
- A result of `None`, `0` or `""` is a valid model result. A falsy `fallback` is returned unchanged.

```python
predict_with_fallback(lambda v: v * 2, 4, -1, 0.1, clock)   # (8, "model") if fast
```

## Library notes

- `time.monotonic()` returns a `float` of seconds. Gotcha: its zero point is arbitrary, so only differences are meaningful. `time.time()` can jump when the system clock is adjusted.
- `try / except Exception as e` catches ordinary errors. Gotcha: bare `except:` would also swallow `KeyboardInterrupt`.
- `try / except / else` runs the `else` block only when no exception happened. Gotcha: an error raised inside `else` is not caught by the same `except`.

## Gotchas

- This pattern measures lateness after the fact. It does not interrupt a slow call, so a hung model still blocks the caller. A real service also needs a hard timeout at the client or thread level.
- Retrying inside a deadline burns the budget and amplifies load on a struggling model.
- Count the paths (`model`, `timeout`, `error`) as metrics. A rising fallback rate is an incident that the users cannot see.
