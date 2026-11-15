Add an optional fifth parameter `valid=None`: `predict_with_fallback(features, model, rule, default, valid=None)`. When `valid` is given, it is a function that takes a stage's value and returns true or false. A stage whose value is not `None` but for which `valid(value)` is false is skipped, like a stage that raised. `valid` is not called for `None` values, and it does not apply to `default`. With `valid` not given, nothing changes.

For example `predict_with_fallback({}, lambda f: 1.7, lambda f: 0.4, 0.1, valid=lambda v: 0 <= v <= 1)` returns `(0.4, "rule")`.
