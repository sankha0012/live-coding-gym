Add a strict mode. Change the signature to `check_health(checks, strict=False)`.

- With `strict=False` (the default) nothing changes.
- With `strict=True`, a `"degraded"` check makes the overall status `"down"` instead of `"degraded"`. The reasons list stays exactly the same (a degraded check still gives `"<name>: degraded"`).

Example: `check_health([("cache", lambda: "degraded")], strict=True)` returns `{"status": "down", "reasons": ["cache: degraded"]}`. With only `"ok"` checks, strict mode still returns `"ok"`.
