# Test `retry`

`retry(fn, tries, sleep)` calls `fn()` (no arguments) until it succeeds, at most `tries` times in total (`tries` is at least 1).

- If a call returns, `retry` returns that value at once and does not call `fn` again.
- If a call raises an exception, `retry` waits by calling `sleep(1)` and tries again.
- It never calls `sleep` after the last failed attempt.
- If every attempt fails, it raises the exception from the last attempt.

`sleep` is passed in, so tests use a fake that only records its calls (for example `calls.append`). Never really sleep in tests.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import retry
