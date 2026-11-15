Let a run do only part of the work. Change the signature to `run_batch(items, handler, store, limit=None)`.

- With `limit=None` (the default) nothing changes.
- With a number, process at most `limit` new items in this call (items that were already done in earlier runs do not count), then return `store["results"]`. The checkpoint is left after the last item processed, so the next call continues from there.
- `limit=0` calls `handler` zero times.

Example: `run_batch([1, 2, 3, 4, 5], h, store, limit=2)` processes 1 and 2 and returns their two results with `store["next"] == 2`. Calling it again with `limit=2` processes 3 and 4, and a third call processes 5 only.
