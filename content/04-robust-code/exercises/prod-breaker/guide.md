**Why this matters.** When a dependency is down, every caller waiting on it and retrying makes the outage worse. A circuit breaker fails fast to a safe fallback, then probes the dependency now and then to notice when it recovers.

**How we get there.**
1. Keep two facts: a failure count, and `opened_at`, the time the breaker opened (`None` means closed). Time comes from the injected `clock()`.
2. At the start of `call`, if `opened_at` is set and less than `cooldown` seconds have passed, return the fallback without touching `fn`. That is the open state.
3. Otherwise try `fn()`. If the cooldown has passed we land here with `opened_at` still set: this is the half-open state, one trial call.
4. On success, reset `failures` to 0 and `opened_at` to `None`, then return the result. The breaker closes.
5. On an exception, add one to `failures`. Open (set `opened_at = clock()`) if the count reached `max_failures` or if this was the trial call, then return the fallback.

**Check it.** A failed trial restarts the full cooldown.

**Watch out.** Forgetting that a failed half-open trial must reopen immediately, even though the failure count may be below the limit.
