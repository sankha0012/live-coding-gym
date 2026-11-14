A nightly scoring job crashes halfway. Write `run_batch(items: list, handler, store: dict) -> list` so that a second run continues where the first stopped.

- `store` is a plain dict that survives the crash. It holds the checkpoint under the keys `"next"` (index of the next item to process, default 0) and `"results"` (list of results so far, default empty).
- Process `items` in order, starting at `store["next"]`. For each item call `handler(item)` once.
- After `handler` returns, record its result and advance the checkpoint. Do this only after success, so a result is never lost and a finished item is never done twice.
- If `handler` raises, let the exception propagate. Leave the checkpoint at the failed item, so the next run tries that item again and then continues.
- Return `store["results"]`. If everything is already done, return it without calling `handler`.
- An empty `items` list returns `[]`.
