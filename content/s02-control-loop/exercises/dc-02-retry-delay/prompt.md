Write `retry(fn, *, attempts, base_ms, cap_ms, sleep)`. It calls `fn()` with no arguments and returns its result. If `fn` raises an exception, wait and try again, up to `attempts` calls in total. The wait after the n-th failed call (n starting at 1) comes from the `backoff` helper, and is passed to `sleep`, which is injected so tests need not really wait.

If every attempt fails, raise the last exception. Do not sleep after the final failed attempt, because there is nothing left to wait for.

Use the `backoff` helper for the delay. Documentation is available below the task, consult it. Check the units of what you pass in and of what you get back.
