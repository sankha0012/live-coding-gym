**Why this matters.** A scoring job may read millions of records, so it cannot hold them all in memory. It also should not die because record 3,000,017 is malformed.

**How we get there.**
1. Reject `chunk_size < 1` first with a `ValueError`, since a chunk of zero would read nothing and quietly return empty results for any input.
2. Turn the input into an iterator with `iter(records)`, and take the next piece with `list(islice(it, chunk_size))`. An empty piece means the input is finished.
3. Try `handle_batch(batch)` on the whole chunk and extend `results`. 
4. Only if it raises, call `handle_batch([record])` for each record of that chunk. Failures go to `errors` as `{"index", "error"}`, where the index is the running offset plus the position in the chunk.
5. After each chunk, add `len(batch)` to the running offset.

**Check it.** Empty input gives `([], [])`. Time is linear in the records, with a second pass over a chunk only when it fails; memory is one chunk plus the output.

**Watch out.** Recording one error for the whole chunk, stopping at the first bad record, or calling `list(records)` up front all break the point of the exercise.
