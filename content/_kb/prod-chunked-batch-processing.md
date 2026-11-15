---
title: Chunked batch processing and isolating bad records
summary: Read a large input in fixed-size chunks and keep one bad record from failing the whole run.
tags: [production, batch]
---
```python
from itertools import islice
def chunks(items, size):
    it = iter(items)
    while batch := list(islice(it, size)):
        yield batch
def run(items, handle, size):
    ok, bad = [], []
    for batch in chunks(items, size):
        for item in batch:
            try:
                ok.append(handle(item))
            except Exception as e:
                bad.append((item, type(e).__name__))
    return ok, bad
```

- Use it when the input does not fit in memory or one failure must not stop the job.
- Key rule: read lazily, bound the chunk size, and return failures next to results.
- Say: "Memory is bounded by the chunk size, and every bad record is reported, not hidden."

<!-- more -->

## Details

`islice(it, size)` takes the next `size` items from the same iterator, so nothing is read twice and the whole input is never in a list. The last chunk may be shorter. Python 3.12 also has `itertools.batched`, which yields tuples.

```python
list(chunks(range(5), 2))             # [[0, 1], [2, 3], [4]]
list(chunks([], 2))                   # []
run(["1", "x", "3"], int, size=2)     # ([1, 3], [('x', 'ValueError')])
```

When the handler works on a whole batch (one model call, one bulk insert), a single bad record fails the batch. The usual answer is two levels: try the batch, and if it raises, retry its records one at a time. Good records in that batch still succeed, and only the truly bad ones go to the error list. This costs extra calls only for batches that fail.

Things to decide and say:

- **Order.** Results in input order. Keep the global index of each record, not its index inside the chunk.
- **Error detail.** Store the position, the error type and the message, so the record can be found and replayed.
- **Too many failures.** A failure rate above a threshold usually means a systemic problem. Stop and alert.
- **Validation.** `size < 1` must raise, or `islice` returns nothing and the loop ends silently.

## Common mistakes

- Calling `list(items)` or `len(items)` on the input, which defeats the streaming.
- Using `range(0, len(items), size)` on something that is a generator.
- Reporting the index inside the chunk instead of the index in the whole input.
- Catching the error and dropping the record with no trace.
- Stopping at the first bad record when the task says to continue.

## See also

- [Iterators and generators](#/kb/py-iterators-generators)
- [itertools: chain, islice, accumulate, groupby, pairwise](#/kb/py-itertools)
- [Checkpointing and resuming a batch](#/kb/prod-checkpointing)
- [Input validation and data contracts](#/kb/prod-input-validation)
