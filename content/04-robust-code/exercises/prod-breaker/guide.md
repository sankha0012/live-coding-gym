**Why this matters.** When a dependency is down, every caller waiting on it and retrying makes the outage worse. A circuit breaker fails fast to a safe fallback, then now and then probes to notice recovery.

**How we get there.**
1. Keep a failure count and `opened_at`, the time it opened (`None` means closed), read from the injected `clock()`.
2. At the start of `call`, if `opened_at` is set and less than `cooldown` seconds have passed, return the fallback without touching `fn`. That is the open state.
3. Otherwise try `fn()`. With `opened_at` still set, the cooldown has passed: the half-open state, one trial call.
4. On success, reset `failures` to 0 and `opened_at` to `None`, then return the result. The breaker closes.
5. On an exception, add one to `failures`. Open (set `opened_at = clock()`) if the count reached `max_failures` or this was the trial, then return the fallback.

**Check it.** A failed trial restarts the full cooldown.

**Watch out.** Resetting `failures` when the breaker opens: a failed trial then looks like failure 1 of 3, `opened_at` keeps its old time, and the next call probes again instead of waiting a fresh cooldown.
