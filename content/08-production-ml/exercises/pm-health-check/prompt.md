A model service exposes a `/health` endpoint built from several component checks, for example the model file, the feature store and the database. Write `check_health(checks: list[tuple[str, callable]]) -> dict`.

Each check is a `(name, fn)` pair. `fn()` returns one of the strings `"ok"`, `"degraded"` or `"down"`.

- Run every check, in order. One failing check never stops the others.
- If `fn` raises any exception, that check counts as `"down"` with the reason `"<name>: down (raised <ExceptionClassName>)"`.
- If `fn` returns anything other than the three strings, that check counts as `"down"` with the reason `"<name>: down (invalid result)"`.
- A check that returns `"degraded"` or `"down"` adds the reason `"<name>: degraded"` or `"<name>: down"`. A check that returns `"ok"` adds no reason.
- The overall status is the worst one: `"down"` beats `"degraded"` beats `"ok"`. No checks at all means `"ok"`.

Return `{"status": <overall>, "reasons": <list of reasons in check order>}`.
