Add an option to keep a late answer. Change the signature to `predict_with_fallback(model, x, fallback, deadline_s, clock, keep_late=False)`.

- With `keep_late=False` (the default) nothing changes.
- With `keep_late=True`, a call that returned normally but took more than `deadline_s` seconds returns `(model_result, "late")` instead of `(fallback, "timeout")`.
- Calls that finish in time still return `(model_result, "model")`. Calls that raise still return `(fallback, "error")`, whatever `keep_late` is.

Example: a model that takes 2 seconds and returns 8, with `deadline_s=0.5` and `keep_late=True`, gives `(8, "late")`.
