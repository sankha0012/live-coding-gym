A job scores millions of records from an iterator. It must not load them all in memory, and one bad record must not kill the run.

Write `process_stream(records, handle_batch, chunk_size)` that returns `(results, errors)`:

- `records` is any iterable. Read it lazily, `chunk_size` records at a time. Never build a list of the whole input.
- `handle_batch(batch: list) -> list` receives a list of at most `chunk_size` records and returns a list of results of the same length.
- If `handle_batch` raises an `Exception` for a batch, call it again for each record of that batch alone, as `handle_batch([record])`. A record whose single call raises goes to `errors` as `{"index": i, "error": "<ExceptionType>: <message>"}`, where `i` is the position of the record in the whole input (from 0). The other records keep their results.
- `results` holds the results of the successful records, in input order.
- Never stop early. An empty input returns `([], [])`.
- If `chunk_size < 1`, raise `ValueError`.
