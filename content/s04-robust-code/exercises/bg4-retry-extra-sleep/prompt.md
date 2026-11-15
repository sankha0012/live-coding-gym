Calling another service fails in two ways. Transient errors (a timeout, a dropped connection) may work on the next try. Permanent errors (a bad request, a bug) never will, and retrying them only wastes time and hides the problem.

Write `call_with_retry(fn, retries, sleep, base_delay=1.0)`:

- Call `fn()` and return its result.
- If `fn` raises `TimeoutError`, `ConnectionError` or `TransientError`, wait and try again. At most `retries` retries are allowed, so `fn` is called at most `retries + 1` times.
- Before retry number `k` (starting at 1), call `sleep(base_delay * 2 ** (k - 1))`. Never sleep after the last failed attempt. Do not call the real `time.sleep`; use the `sleep` argument.
- Any other exception is permanent: re-raise it immediately, with no sleep and no retry. This includes other `OSError` types such as `FileNotFoundError`.
- If all attempts fail with a transient error, re-raise the last one.

`TransientError` is already defined for you.

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
