# eventwin: reference

Internal helper for counting events by time. All times are plain numbers in seconds (for example Unix seconds). The module is `eventwin.py`; import it with `from eventwin import window_slice`.

## `window_slice(timestamps, start, end, *, inclusive_end=False)`

- `timestamps`: any iterable of numbers. It does not need to be sorted and may be empty.
- `start`: the lower bound of the window, in seconds.
- `end`: the upper bound of the window, in seconds.
- `inclusive_end`: optional, keyword only, default `False`. When `True`, the window is closed on both sides and an event exactly at `end` is returned as well.

Returns a new list with every `t` for which `start <= t < end` (by default), in the same order as the input. The input is never modified.

### Bounds

By default the window is half-open: `start` is **inclusive** and `end` is **exclusive**. An event exactly at `start` is returned; an event exactly at `end` is not. This way adjacent windows `[a, b)` and `[b, c)` never count an event twice.

### Errors and empty input

- If `end < start` it raises `ValueError`. Arguments are in the order `(timestamps, start, end)`; swapping `start` and `end` raises.
- If `end == start`, the window is empty and the result is `[]`.
- Empty `timestamps` returns `[]`.

### Gotcha

The upper bound is exclusive unless you ask otherwise. To include an event at time `x`, pass `inclusive_end=True`. Passing `end=x` alone silently leaves that event out, and adding a small amount to `end` (such as `x + 1`) also lets in events that come after `x`.

### Example

```python
window_slice([1, 5, 10, 12], 5, 12)                       # [5, 10]
window_slice([1, 5, 10, 12], 5, 12, inclusive_end=True)   # [5, 10, 12]
```
