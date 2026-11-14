A prediction API receives a JSON request as a dict. Write `validate_request(request: dict, contract: dict) -> tuple[dict, list[str]]` that checks it against a contract and returns `(clean, violations)`.

The contract maps a field name to a rule dict. A rule has `"type"` (`int`, `float` or `str`), optional `"required"` (default `False`), and optional `"min"` and `"max"` (inclusive, used only for `int` and `float`).

```python
contract = {
    "user_id": {"type": str, "required": True},
    "age": {"type": int, "required": True, "min": 0, "max": 120},
    "score": {"type": float, "min": 0.0, "max": 1.0},
}
```

Rules, checked per field in contract order:
- A field that is absent or `None` is missing. If it is required, add `"missing:<field>"`. If it is optional, skip it silently.
- A value of the wrong type adds `"bad_type:<field>"`. A `bool` is not an `int` or a `float`. An `int` is accepted for a `float` field and is converted with `float()`.
- A number below `min` or above `max` adds `"out_of_range:<field>"`. A float `nan` is always `"out_of_range:<field>"`.
- A field with a violation is left out of `clean`. A field that passes goes into `clean`.
- Fields in the request that are not in the contract are dropped. Never change the input dicts.

`violations` lists every problem, not just the first, in contract order. A clean request gives an empty list.
