# predict_with_fallback reference

## Contract

`predict_with_fallback(features, model, rule, default) -> tuple[value, str]`

`model` and `rule` are callables taking `features` and returning a number. Stages are tried in order: `model`, then `rule`, then the constant `default`. The result is `(value, stage)` with `stage` one of `"model"`, `"rule"`, `"default"`.

A stage is skipped when it raises any `Exception` or returns `None`. Any other return, including `0` and `0.0`, is accepted. A stage that answers ends the chain: later stages are not called. Each called stage receives `features` unchanged. `default` is returned as is, even when it is `None`.

```
predict_with_fallback({"a": 1}, lambda f: None, lambda f: 0.0, 0.1)
# (0.0, "rule")
```

## Library notes

- `try / except Exception`: catches ordinary errors such as `KeyError` or `TypeError`. It does not catch `KeyboardInterrupt` or `SystemExit`, which derive from `BaseException`.
- `x is None`: exact test for `None`. `if not x` also matches `0`, `0.0` and `False`.
- A bare `except:` catches `BaseException` too, which would swallow Ctrl-C and shutdowns.
- `callable(obj) -> bool`: True if the object can be called. A stage that is not callable raises `TypeError` when called, which counts as a failure.

## Gotchas

- Falling back silently hides outages. Record which stage answered so a rising share of `"rule"` or `"default"` is visible.
- A slow model is not an error. In production add a timeout, otherwise the fallback never triggers.
- Returning NaN is an answer here, not a failure, unless you decide otherwise explicitly.
