**Why this matters.** A nightly job over thousands of items will crash somewhere in the middle. We do not want to start over, and we do not want to score an item twice or lose a finished result.

**How we get there.**
1. Keep the progress inside `store`, which survives the crash. `store.setdefault("results", [])` and `store.setdefault("next", 0)` create the checkpoint on a first run and leave it alone on a resume.
2. Loop with `while store["next"] < len(items)`. Starting from the stored index is the whole resume mechanism.
3. Call `handler(items[store["next"]])` once per pass.
4. Only after the handler returns, append the result and do `store["next"] += 1`.
5. Return the results list. If everything was done already, the loop body never runs.

**Check it.** If the handler raises, the exception leaves the loop before the two updates, so the checkpoint still points at the failed item and the next run retries it.

**Watch out.** Advancing the index before the handler runs means a crash skips that item for ever. A crash after the handler's side effect but before the checkpoint write still repeats the item, so handlers should be safe to repeat.
