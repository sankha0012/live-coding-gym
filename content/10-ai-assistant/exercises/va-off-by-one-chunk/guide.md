**Why this matters.** Splitting a list into batches is routine, and the usual bug silently loses the end of the data. Nothing crashes, the last items just never get processed.

**How we get there.**
1. Reproduce with `chunk([1, 2, 3, 4, 5], 2)`. We expect `[[1, 2], [3, 4], [5]]` but get `[[1, 2], [3, 4]]`. An exact multiple loses its last chunk too.
2. Locate it: `range(0, len(items) - size, size)` stops `size` positions too early, so the final start index is never visited.
3. Fix the bound to `len(items)`, so every multiple of `size` below the length is a start index.
4. Keep the slice `items[i:i + size]`. A slice past the end is safe in Python and returns the short remainder, so the last chunk needs no extra code.

**Check it.** An empty list gives an empty range, so `[]`. Every item lands in exactly one chunk, and the input is only read. Time and space are linear.

**Next time.** Test the boundary sizes: empty, one item, an exact multiple and a remainder.

**Watch out.** Adding a special case for the tail often produces an empty trailing chunk.
