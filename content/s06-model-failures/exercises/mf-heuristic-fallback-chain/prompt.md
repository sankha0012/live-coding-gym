A production service should still answer when the model is down. Write `predict_with_fallback(features, model, rule, default)`.

`model` and `rule` are functions that take `features` and return a number. Try `model` first, then `rule`, then use the constant `default`. Return a tuple `(value, stage)` where `stage` is `"model"`, `"rule"` or `"default"`.

A stage is skipped, and the next one is tried, when it raises any `Exception` or returns `None`. Any other return value is accepted, including `0` and `0.0`. Do not call a later stage if an earlier one answered. `default` is returned as is, even if it is `None`.
