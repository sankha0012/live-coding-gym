**Why this matters.** Splitting a list into batches comes up with API limits, bulk inserts and pagination. Python slicing makes the code short, but the bad input needs a decision.

**How we get there.**
1. Reject a bad size first: if `n <= 0`, raise `ValueError`. With `n = 0`, `range` would fail with a confusing message, and with a negative `n` it would quietly return no chunks.
2. Compute where each chunk starts: `range(0, len(items), n)` gives 0, n, 2n, and so on.
3. Slice `n` items from each start: `items[i:i + n]`. A slice that runs past the end just stops, so the last chunk is shorter with no extra code.
4. Wrap it in a list comprehension to get the list of chunks.

**Check it.** An empty list gives `[]`, and an `n` larger than the list gives one chunk with everything. The check for `n` comes before anything else, so even `chunks([], 0)` raises. It is O(len(items)), and slices copy, so the input is not changed.

**Watch out.** Skipping the validation lets `n = 0` crash with an obscure `range` error, and looping only over full chunks drops the short last chunk.
