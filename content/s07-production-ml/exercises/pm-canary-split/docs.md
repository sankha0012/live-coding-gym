# assign_arm: reference

## Contract

`assign_arm(user_id: str, canary_percent: int = 5, salt: str = "canary-v1") -> str` returns `"canary"` or `"stable"`.

- The bucket is an integer from 0 to 99: hash the text `f"{salt}:{user_id}"` with `hashlib`, read the digest as an integer, and take it modulo 100.
- The user is in the canary when `bucket < canary_percent`. At 0 nobody is in the canary, at 100 everybody is.
- The result depends only on the three arguments. It is identical across processes, machines and days.
- Raising `canary_percent` only adds users. A user in the canary at 5 is still there at 10.
- Changing `salt` reshuffles who is in the canary. The share stays close to `canary_percent` over many ids.
- An empty `user_id` is legal and gets an arm like any other.

```python
assign_arm("user-1", 50)   # always the same answer for this input
```

## Library notes

- `hashlib.sha256(data: bytes)` returns a hash object, and `.digest()` returns `bytes` while `.hexdigest()` returns `str`. Gotcha: it needs `bytes`, so a `str` must be encoded first with `.encode()`.
- `int(text, 16)` parses a hex string and returns an `int`. Gotcha: you must pass the base, or it will try to parse base 10.
- `int.from_bytes(b, "big")` returns an `int` from raw bytes. Gotcha: the byte order argument is required, and it changes the number.

## Gotchas

- The built-in `hash()` of a `str` is randomized per process (`PYTHONHASHSEED`). Using it makes users hop between arms on every restart or between workers.
- Changing the salt mid-rollout moves everyone to new arms. Keep it fixed for a rollout and change it only to start a new experiment.
- Bucketing on user id keeps a user's experience stable, but anonymous traffic with no id cannot be bucketed this way.
