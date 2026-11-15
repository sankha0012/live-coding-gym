# fill_features reference

## Contract

`fill_features(row: dict, defaults: dict) -> tuple[dict, list[str]]`

`defaults` maps feature name to its fallback value. A feature is missing when its key is absent from `row` or its value is `None`. Nothing else is missing: `0`, `0.0`, `False` and `""` are real values and stay as they are.

Output is `(filled_row, filled_names)`. `filled_row` has every key of `defaults` plus any extra keys of `row`, which are kept unchanged. `filled_names` is the sorted list of features that were filled.

```
fill_features({"items": None, "promo": "x"}, {"items": 1, "km": 3.0})
# ({"items": 1, "promo": "x", "km": 3.0}, ["items", "km"])
```

Neither `row` nor `defaults` is modified. An empty row returns all defaults, with all names filled.

## Library notes

- `dict.get(key, default=None) -> value`: returns `None` both for an absent key and for a key whose value is `None`, so it cannot tell them apart.
- `dict.copy()` or `dict(d) -> dict`: a shallow copy. The new dict is independent, but nested lists or dicts are shared.
- `sorted(iterable) -> list`: returns a new list. Names here are strings, so the order is alphabetical.
- `x is None` tests for `None` exactly. `not x` is also true for `0`, `""` and `False`.

## Gotchas

- Truthiness checks (`if not value`) treat a legitimate zero as missing and quietly replace real data.
- Filling hides upstream outages. Return which features were filled so the caller can log or alert on a rising rate.
- Mutable defaults (lists, dicts) put into a row are shared between requests. Copy them if they could be mutated later.
