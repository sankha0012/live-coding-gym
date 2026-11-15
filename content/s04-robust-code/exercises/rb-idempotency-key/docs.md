## Contract

`class IdempotentRunner(func)` with method `run(key, payload)`.

- `func` takes one argument, the payload. The constructor only stores it and calls nothing.
- The first `run` with a new `key` calls `func(payload)` once and returns its result.
- Any later `run` with the same `key` returns the stored result without calling `func` and ignores the new payload. The key alone identifies the request.
- If the first call raised, that exception object is remembered. Every later `run` with the same key raises the very same object (an identity check passes) and does not call `func`, whatever the payload.
- Different keys are independent: one key failing does not affect another.
- Keys are any hashable value, including falsy ones such as `0`, `""`, `None` and `()`, or tuples like `("user", 1)`.
- Results may be anything, including `None`, `0`, `""`, `[]` and `False`. A stored falsy result still counts as stored.
- Each runner has its own memory; two runners never share results.

## Library notes

- `key in d` returns a bool and works for any hashable key; `d.get(key)` returns `None` both for a missing key and for a stored `None`, so it cannot tell them apart without a sentinel such as `object()`.
- `d[key] = value` stores or replaces; a dict key must be hashable, otherwise `TypeError`.
- `raise exc` re-raises an existing exception object; each raise appends to its `__traceback__`.
- `threading.Lock()` used as `with lock:` lets only one thread inside at a time.

## Gotchas

- Marking a key as seen before the call finishes lets a crash leave it half-recorded.
- Two threads with the same key can both pass a check-then-act; real systems need a lock or an atomic store.
- Stored results grow without bound; production code needs expiry.
