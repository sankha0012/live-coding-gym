A real-time service must always answer. Write `predict_with_fallback(model, x, fallback, deadline_s, clock) -> tuple` that calls `model(x)` once and returns `(value, path)`.

- `clock` is a function that returns the current time in seconds. Read it before and after the call. Never read the real clock.
- If the call returned normally and took at most `deadline_s` seconds, return `(model_result, "model")`.
- If the call took more than `deadline_s` seconds, the late result is too old to use: return `(fallback, "timeout")`.
- If `model(x)` raises any `Exception`, return `(fallback, "error")`. Do not retry and do not let the exception escape.
- `model` is called exactly once in every case.
- A model result that happens to be `None` or `0` is still a valid result on the `"model"` path.
