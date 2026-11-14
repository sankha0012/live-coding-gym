A payment worker can receive the same request twice (client retries, queue redelivery). Write the class `IdempotentRunner` that makes sure each request key runs once.

- `IdempotentRunner(func)` stores the function.
- `run(key, payload)` calls `func(payload)` the first time it sees `key` and returns the result.
- On the same `key` again, return the stored result. Do not call `func` again, and ignore the new payload.
- If the first call raised an exception, remember it. On the same `key` again, raise that same exception object and do not call `func` again.
- Different keys are independent.
- Keys are hashable values. A result may be `None`, and a repeat still must not call `func`.
