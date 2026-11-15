# score_batch reference

## Contract

`score_batch(rows, score_fn) -> dict`

`score_fn(row)` returns a score or raises an exception for a bad row. It is called once per row, in input order.

The result has two keys:

- `"scores"`: one entry per input row, same order and length. Good rows hold their score (including `0`), bad rows hold `None`.
- `"errors"`: one `{"index": i, "reason": "<ExceptionName>: <message>"}` per bad row, in input order.

```
# score_fn raises ValueError("price is negative") for row 1
{"scores": [2, None], "errors": [{"index": 1, "reason": "ValueError: price is negative"}]}
```

Only `Exception` is caught. `KeyboardInterrupt` and `SystemExit` propagate. Empty `rows` gives `{"scores": [], "errors": []}`.

## Library notes

- `type(e).__name__ -> str`: the exception class name, for example `"KeyError"`.
- `str(e) -> str`: the message. Gotcha: for `KeyError("price")` it is `'price'` with the quotes, and for an exception raised without arguments it is the empty string.
- `enumerate(iterable, start=0) -> iterator of (index, item)`: gives the position for the error record.
- `except Exception as e`: `e` is deleted when the block ends, so format the text inside the block.

## Gotchas

- Catching too narrowly lets one odd row kill the batch. Catching `BaseException` makes the service impossible to stop.
- Keep positions aligned with the input. Dropping bad rows would shift every later score onto the wrong row.
- Watch the error rate. If most rows fail, the cause is usually upstream, not the rows.
