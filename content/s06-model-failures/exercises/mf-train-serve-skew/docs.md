# serve_features reference

## Contract

`serve_features(row: dict, stats: dict) -> dict`

Takes one row and returns exactly what `train_features([row], stats)[0]` returns, with the same keys: `{"amount_z": float, "category": str}`. Extra keys in `row` are ignored. `train_features` is the reference and is not changed.

`stats` is `{"mean": float, "std": float}`. The reference rules:

- `amount`: absent or `None` counts as `0.0`. Then `math.log1p(amount)`, then `(value - mean) / std`.
- `category`: strip surrounding whitespace, lowercase. Absent, `None` or `""` becomes `"unknown"`. A string of only spaces is not missing: it becomes `""`.

```
stats = {"mean": 2.0, "std": 1.5}
{"amount": 0.0, "category": " A "}  ->  {"amount_z": -4/3, "category": "a"}
```

## Library notes

- `math.log1p(x) -> float`: computes `log(1 + x)`. It is defined at `0`. `math.log(0)` raises `ValueError`, and `math.log(x)` differs from `log1p(x)` for every `x`.
- `dict.get(key, default=None)`: returns `None` for an absent key, so it cannot distinguish absent from `None`. It does not raise `KeyError`.
- `str.strip()` and `str.lower()` return new strings, and `str.strip()` turns `"   "` into `""`.
- `a or b`: returns `b` when `a` is falsy, and `""` is falsy but `"   "` is not. Order of operations changes the result.

## Gotchas

- Training and serving drift silently. Models degrade with no exception, so test them against one shared reference on the same rows.
- Missing values must be handled the same way at both ends, including what counts as missing.
- Fix the serving code to match, never the reference, since the model learned from the reference.
