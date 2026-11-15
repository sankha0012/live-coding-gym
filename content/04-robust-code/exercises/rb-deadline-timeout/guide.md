**Why this matters.** A nightly batch has a time budget. If it runs until it is killed, items are left half done and nobody knows what to redo. We want to stop cleanly and hand back what is left.

**How we get there.**
1. Copy the input with `list(items)`, so we can slice it later and also accept any iterable without changing the caller's data.
2. Loop with `enumerate`, so we always know the position `i`.
3. At the top of each turn, ask `clock() >= deadline`. We use the injected clock, never the real one, so time can be controlled exactly.
4. If time is up, return `results, items[i:]`: what we finished, and the items we never started, in order.
5. Otherwise append `handler(item)` to the results. If the loop ends, nothing remains: return `results, []`.

**Check it.** Because the check comes before the handler, a started item always finishes, and an already-passed deadline returns `([], list(items))`. Handler exceptions simply propagate.

**Watch out.** Checking after the handler runs one item too many, and using `>` instead of `>=` lets a new item start exactly at the deadline.
