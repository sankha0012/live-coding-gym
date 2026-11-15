`batch_split(items, n)` splits a list into consecutive batches of size `n` and returns a list of lists.

- Every batch has exactly `n` items, except the last one, which may be shorter.
- The order of the items is kept. No batch is ever empty.
- An empty list gives an empty list of batches.
- If `n` is less than 1, raise `ValueError`.
- The input list is not modified.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import batch_split
