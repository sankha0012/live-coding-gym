# backoff: reference

Internal helper that computes how long a retry loop should wait between attempts. The module is `backoff.py`; import it with `from backoff import backoff_delay`.

## `backoff_delay(attempt, base_ms, cap_ms, factor=2)`

Exponential backoff: the wait doubles after every failure until it reaches a cap.

- `attempt`: the number of the attempt that just failed, counted from **1**. The first failure is `attempt=1`.
- `base_ms`: the delay after the first failure, in **milliseconds**.
- `cap_ms`: the largest delay allowed, in **milliseconds**.
- `factor`: optional, default `2`. The number by which the delay is multiplied after every failure. With `factor=3` the delays are `base_ms`, `3 * base_ms`, `9 * base_ms`, and so on, up to the cap.

### Return value

Returns the number of **seconds** to wait, as a float. The formula is `min(base_ms * factor ** (attempt - 1), cap_ms) / 1000`. With `base_ms=100` and `cap_ms=5000`, attempts 1, 2, 3 return `0.1`, `0.2`, `0.4`, and from attempt 7 onward the result stays at `5.0`.

### Errors

- `attempt < 1` raises `ValueError`. There is no attempt 0.
- The helper does not sleep and does not retry anything. It only does the arithmetic; the caller decides what to do with the number.

### Gotcha: units differ between input and output

Inputs are milliseconds, the return value is seconds. That matches `time.sleep`, which takes seconds, so the returned value can be passed straight to a sleep function. Do not divide it by 1000 again, and do not multiply it.

### Example

```python
backoff_delay(1, 100, 5000)   # 0.1
backoff_delay(3, 100, 5000)   # 0.4
backoff_delay(10, 100, 5000)  # 5.0
backoff_delay(3, 100, 5000, factor=3)  # 0.9
```
