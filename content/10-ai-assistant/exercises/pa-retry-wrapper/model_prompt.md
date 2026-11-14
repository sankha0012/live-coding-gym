Write a Python function `call_with_retry(fn, max_attempts=4, base_delay=0.5, retry_on=(TimeoutError, ConnectionError), sleep=time.sleep)` that calls `fn()` and returns its result.

Behaviour:
- If `fn` raises one of the `retry_on` exceptions, wait and try again. The wait before retry k is `base_delay * 2**(k-1)`: 0.5, 1.0, 2.0 seconds.
- After `max_attempts` failed attempts, re-raise the last exception. Do not wrap it.
- Any other exception, such as ValueError for a bad request, is raised immediately with no retry.
- The `sleep` function is a parameter so tests never really wait. No wall clock, no unseeded randomness. If you add jitter, take a seeded `random.Random` as a parameter and make it optional.
- `max_attempts` below 1 raises ValueError.

Also write pytest tests with a fake `fn` that fails N times and a fake `sleep` that records its arguments. Test: success on the first try (no sleep), success after two failures (sleeps 0.5 and 1.0), all attempts fail (last error re-raised, 3 sleeps for 4 attempts), a non-retryable error (one call, no sleep) and invalid `max_attempts`.

Finally explain in a few sentences why backoff is exponential and one risk of retrying a call that is not idempotent.
