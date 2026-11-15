# featurestore: reference

Internal read-only client for the feature store. Each entity id (a string such as `"u1"`) has one numeric feature. The module is `featurestore.py`; import it with `from featurestore import get_features`.

## `get_features(keys, *, default=...)`

Looks up several entities at once.

- `keys`: an iterable of entity ids. It may contain duplicates and unknown ids.
- `default`: keyword-only and optional. It cannot be passed positionally; `get_features(keys, 0.0)` raises `TypeError`.

### Return value

Returns a plain `dict` mapping entity id to feature value.

- Without `default`, an entity that is **not in the store is left out** of the dict. It is not mapped to `None`, and no error is raised. The dict may therefore have fewer entries than `keys`, and a lookup like `result["u9"]` raises `KeyError`.
- With `default=x`, every absent id is present in the dict and maps to `x`. `default=None` is allowed and means the value `None` is stored for absent ids.
- The order of the dict is not a contract; do not rely on it matching the order of `keys`. Duplicate keys collapse into a single entry.
- An empty `keys` returns `{}`.

### Stored values

Values are floats. A stored value can legitimately be `0.0`; that is a real measurement, not "missing".

### Errors

The helper itself never raises for unknown ids. It only raises `TypeError` for the misuse above.

### Gotcha

Absence means a missing dict key, not a `None` value. Test with `in` or pass `default`, not with `is None`.

### Example

```python
get_features(["u1", "u9"])                # {"u1": 0.5}
get_features(["u1", "u9"], default=-1.0)  # {"u1": 0.5, "u9": -1.0}
```
