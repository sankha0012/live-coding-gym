**Why this matters.** An audit that picks "random" records must be repeatable, so a reviewer can run it again and get the same ids. The trap is that seeding the global generator repeatable-izes this call but also resets the random state for every other part of the program.

**How we get there.**
1. Do not call `random.seed(seed)`. That changes shared state, and other code drawing random numbers would change our result, and we would change theirs.
2. Make a private generator with `random.Random(seed)`. It has its own state, fully determined by the seed.
3. Call its `.sample(population, k)`, which picks `k` different positions with no repeats.
4. Pass `list(ids)`, so we hand it a sequence and never touch the caller's list. We do not shuffle the input either.

Together: `random.Random(seed).sample(list(ids), k)`.

**Check it.** `k == 0` gives `[]`, and a negative `k` or one above `len(ids)` makes `sample` raise `ValueError`, as required. The copy costs linear time. Exact picks are stable for a given Python version, so store the seed with the result.

**Watch out.** Using the global seed, forgetting to pass the seed at all, or shuffling the input in place each break one of the promises.
