**Why this matters.** Logs that people search by hand as text become logs that machines filter by field. A record is a flat dict, and the danger is that a caller's own field named `level` or `ts` silently replaces the real one.

**How we get there.**
1. Validate before building anything. `level` must be in a small set, and `event` must be a non-empty string; otherwise raise `ValueError`.
2. Treat `None` fields as empty with `fields = fields or {}`.
3. Check each reserved name (`level`, `event`, `ts`) with `in fields`, and raise `ValueError` naming it. We refuse rather than overwrite, so a bug is loud.
4. Build a new dict in one expression, fixed keys first, then the caller's data: `{"level": level, "event": event, "ts": clock(), **fields}`.
5. The injected `clock` is called exactly once, inside that literal, so one record has one time and tests can control it.

**Check it.** The caller's `fields` is only read, never changed, because we return a fresh dict. Cost is linear in the number of fields.

**Watch out.** Writing the fixed keys into the caller's dict mutates it, and letting `**fields` come last without checking lets a field hide the real level.
