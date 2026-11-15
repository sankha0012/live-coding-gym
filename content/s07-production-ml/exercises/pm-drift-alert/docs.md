# DriftAlert: reference

## Contract

`DriftAlert(high: float, low: float)` is a small stateful object fed one drift score per call (for example an hourly PSI value).

- `update(score) -> str | None` returns `"raised"` when the alert turns on, `"cleared"` when it turns off, and `None` when the state did not change.
- `active` is a `bool` attribute holding the current state. It is `False` on a new object.
- A score strictly above `high` means raised. A score strictly below `low` means cleared. A score from `low` to `high`, both inclusive, never changes the state.
- Repeating a condition that already holds (a high score while active, a low score while inactive) returns `None`.
- `DriftAlert(high, low)` raises `ValueError` when `low > high`. `low == high` is allowed.

```python
a = DriftAlert(0.25, 0.10)
[a.update(s) for s in [0.05, 0.30, 0.20, 0.05]]
# [None, 'raised', None, 'cleared']
```

## Library notes

- `a < b`, `a > b` on floats return `bool`. Gotcha: `<=` and `>=` are not the same test as `<` and `>`; the boundary values are where they differ.
- `isinstance(x, bool)` is true for `True` and `False` only. Gotcha: `bool` is a subclass of `int`, so `isinstance(True, int)` is also true.

## Gotchas

- State lives in the object. One instance per monitored feature or model, never a shared one, or two features will clear each other's alerts.
- Hysteresis only helps if the band is wide enough for the noise. A band narrower than the normal hour-to-hour wobble of the score still flaps.
- A process restart resets `active` to `False`. A score that is still high will fire "raised" again, so downstream consumers should tolerate a repeated alert.
