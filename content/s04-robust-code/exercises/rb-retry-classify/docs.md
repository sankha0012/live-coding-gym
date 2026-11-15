## Contract

`call_with_retry(fn, retries, sleep, base_delay=1.0)`, with `TransientError` already defined in the module.

- `fn` takes no arguments. Its return value is returned on the first success.
- Transient means an instance of `TimeoutError`, `ConnectionError` or `TransientError`, including subclasses such as `ConnectionResetError`. Everything else is permanent, including other `OSError` types (`OSError` itself, `FileNotFoundError`, `PermissionError`).
- A permanent error is re-raised at once: no sleep, no further call, even after earlier transient failures.
- `retries` is the number of extra tries, so `fn` runs at most `retries + 1` times. `retries=0` means one call.
- Before retry `k` (1, 2, ...) the function calls `sleep(base_delay * 2 ** (k - 1))`. With `base_delay=1.0` the waits are 1.0, 2.0, 4.0. There is no sleep after the last failed attempt.
- If every attempt fails with a transient error, the last exception is re-raised unchanged.
- The `sleep` argument is the only way to wait; the real `time.sleep` is not called, which keeps tests instant.

## Library notes

- `except (A, B):` takes a tuple of classes and also matches subclasses of each. The exception hierarchy decides what matches, so check it: `issubclass(ConnectionResetError, ConnectionError)` is True, `issubclass(FileNotFoundError, ConnectionError)` is False, and both are `OSError` subclasses.
- A bare `raise` inside an `except` block re-raises the active exception with its traceback.
- `2 ** n` with an int `n` gives an int; multiplying by a float `base_delay` gives a float.
- `range(n)` yields `0 .. n-1`, so an off-by-one between attempts and retries is easy.

## Gotchas

- Catching `OSError` (or `Exception`) to be safe retries permanent errors and hides bugs.
- Sleeping after the final failure delays the error report for nothing.
- Retrying without a cap on `retries` can multiply load on a service that is already struggling.
