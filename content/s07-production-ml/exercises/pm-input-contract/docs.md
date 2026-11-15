# validate_request: reference

## Contract

`validate_request(request: dict, contract: dict) -> tuple[dict, list[str]]` returns `(clean, violations)`.

The contract maps a field name to a rule dict with `"type"` (`int`, `float` or `str`), optional `"required"` (default `False`), and optional inclusive `"min"` and `"max"`, which apply to `int` and `float` only and are independent of each other.

- Fields are processed in contract order, and violations are listed in that order, all of them.
- A field that is absent or `None` is missing: `"missing:<field>"` if required, silently skipped otherwise. `0` and `""` are values, not missing.
- A wrong type gives `"bad_type:<field>"`. `bool` is neither `int` nor `float`. An `int` is accepted for a `float` field and stored as `float(value)`. A `float` is not accepted for an `int` field.
- A value below `min` or above `max` gives `"out_of_range:<field>"`. A float `nan` is always out of range, even without bounds.
- Fields with a violation are left out of `clean`. Passing fields go in. Fields not in the contract are dropped. The inputs are never modified.

```python
validate_request({"age": 130, "x": 1}, {"age": {"type": int, "max": 120}})
# ({}, ["out_of_range:age"])
```

## Library notes

- `isinstance(v, int)` returns `bool`. Gotcha: `isinstance(True, int)` is `True`, so booleans need a separate check.
- `math.isnan(x)` returns `bool`. Gotcha: it raises `TypeError` for non-numbers, and `nan < 1` and `nan > 1` are both `False`, so range comparisons alone never catch it.
- `dict.get(key)` returns `None` for absent keys. Gotcha: it cannot tell an absent key from an explicit `None`.

## Gotchas

- Validate at the service boundary and score only the cleaned dict. Passing raw input downstream lets unknown or mistyped fields reach the model.
- Silent coercion hides client bugs. Convert only where the contract says so, and report everything else.
