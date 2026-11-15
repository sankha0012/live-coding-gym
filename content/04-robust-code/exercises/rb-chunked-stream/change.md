Add an error budget. Change the signature to `process_stream(records, handle_batch, chunk_size, max_errors=None)`.

- With `max_errors=None` (the default) nothing changes.
- With a number, after each chunk has been fully handled (including the record-by-record retry of a failed chunk), check `len(errors)`. If it is `max_errors` or more, stop: do not read any further chunk, and return the `(results, errors)` collected so far.
- The chunk that reached the limit is still fully handled, so all of its bad records are in `errors`.

Example: `records = range(10)`, `chunk_size=2`, and `handle_batch` raises for any batch that contains a record with `x % 4 == 1` (that is 1, 5 and 9). With `max_errors=2` the run stops after the chunk `[4, 5]`: errors are the indexes 1 and 5, and records 6 to 9 are never read.
