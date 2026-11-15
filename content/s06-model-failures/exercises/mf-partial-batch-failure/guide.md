**Why this matters.** In a batch of thousands of rows, one malformed row should not lose all the other answers. We isolate each failure and report it.

**How we get there.**
1. Loop with `enumerate(rows)`, so we know each row's position.
2. Put the `try` inside the loop, around the single call `score_fn(row)`. Around the whole loop, the first exception would stop everything.
3. On success, append the score. On failure, append `None`. That placeholder keeps `scores` the same length and order as `rows`, so the caller can pair them back up.
4. Record the error too: the index `i` and a reason like `f"{type(e).__name__}: {e}"`, which gives `ValueError: price is negative`.
5. Catch `Exception`, not a bare `except`, so `KeyboardInterrupt` still stops the program.

**Check it.** An empty batch gives two empty lists. One scorer call per row means linear cost.

**Watch out.** Skipping bad rows shifts every later score one place left, and recording the index of good rows instead of bad ones points the caller to the wrong place.
