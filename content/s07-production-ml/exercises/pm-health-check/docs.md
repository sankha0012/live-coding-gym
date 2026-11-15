# check_health: reference

## Contract

`check_health(checks: list[tuple[str, callable]]) -> dict`. Each item is `(name, fn)`, and `fn()` is expected to return `"ok"`, `"degraded"` or `"down"`.

- Every check runs exactly once, in list order. A failing check never stops the later ones.
- If `fn` raises any exception, the check counts as down with the reason `"<name>: down (raised <ExceptionClassName>)"`.
- If `fn` returns anything other than those three exact strings (wrong case, `None`, `True`, a list), the check counts as down with the reason `"<name>: down (invalid result)"`.
- A `"degraded"` or `"down"` result adds `"<name>: degraded"` or `"<name>: down"`. An `"ok"` result adds no reason.
- The overall status is the worst one, `down` over `degraded` over `ok`. An empty list is `"ok"`.
- The return value is `{"status": <overall>, "reasons": [<reasons in check order>]}`.

```python
check_health([("db", lambda: "ok"), ("cache", lambda: "degraded")])
# {"status": "degraded", "reasons": ["cache: degraded"]}
```

## Library notes

- `type(exc).__name__` returns the class name as a `str`, such as `"KeyError"`. Gotcha: `str(exc)` is the message, not the class.
- `try: ... except Exception as e:` catches ordinary errors. Gotcha: it does not catch `KeyboardInterrupt` or `SystemExit`, and `e` is deleted after the block ends.
- `x in ("a", "b")` tests membership in a tuple. Gotcha: it compares with `==`, so it is safe for unhashable values, unlike a set lookup, which raises `TypeError` for a list.

## Gotchas

- A health check that hangs is worse than one that fails. In production give each check its own timeout.
- Keep the endpoint cheap. Orchestrators call it every few seconds, so heavy checks should read a cached result.
- Do not expose exception messages publicly. They can leak hostnames or credentials, which is why the reason only carries the class name.
