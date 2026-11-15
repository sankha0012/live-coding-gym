**Why this matters.** Unit mistakes (milliseconds versus seconds) and off-by-one attempt numbers are classic production bugs, and the assistant will not warn you about them in a helper it has not read. The docs are the source of truth.

**How we get there.**
1. Read `docs.md`: `backoff_delay(attempt, base_ms, cap_ms)`, attempts start at 1, inputs are milliseconds, the return value is seconds.
2. Loop `attempt` from 1 to `attempts`. Call `fn()` inside `try`; on success return its value.
3. On an exception, if this was the last attempt, re-raise it (this keeps the last exception).
4. Otherwise call `sleep(backoff_delay(attempt, base_ms, cap_ms))`. The value is already in seconds, so no conversion is needed.

**Check it.** With `base_ms=100`, three failures give sleeps of `0.1, 0.2, 0.4`. Three attempts that all fail sleep only twice.

**Watch out.** A zero-based loop variable makes the helper raise `ValueError`. Converting seconds again, or sleeping after the last failure, is wrong as well.
