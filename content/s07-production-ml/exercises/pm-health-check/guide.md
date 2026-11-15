**Why this matters.** A health endpoint is what the load balancer and the on-call person look at. If one broken dependency makes the check itself crash, you get a useless 500 instead of a clear report.

**How we get there.**
1. Give each status a number, `{"ok": 0, "degraded": 1, "down": 2}`, so the worst one is simply the biggest.
2. Loop over the pairs in order so every check runs.
3. Put only `result = fn()` inside `try`. If it raises, the check counts as `"down"` with the reason `"<name>: down (raised <ExceptionClassName>)"`.
4. In the `else` branch, a result outside the three allowed strings is down with `(invalid result)`. A valid non-ok result adds `"<name>: <status>"`, and `"ok"` adds nothing.
5. After each check, keep the worse of the current worst and this result. Return the status with the list of reasons.

**Check it.** No checks leaves the status at `"ok"` with no reasons. Keeping a maximum means check order never changes the overall status.

**Watch out.** Wrapping the whole body in `try` can hide your own bugs, and a check that returns `None` or `True` must count as down, not as healthy.
