Write `score_batch(rows, score_fn)`. `score_fn(row)` returns a score, or raises an exception when the row is bad. One bad row must not sink the whole batch.

Return a dict with two keys:

- `"scores"`: a list with one entry per input row, in the same order. Good rows hold their score. Bad rows hold `None`.
- `"errors"`: a list of `{"index": i, "reason": "<ExceptionName>: <message>"}`, one per bad row, in input order. For example `{"index": 2, "reason": "ValueError: price is negative"}`.

Catch `Exception` only. An empty `rows` returns `{"scores": [], "errors": []}`.


An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
