A batch job must stop starting new work when its time budget is over. Write `process_until(items, handler, deadline, clock)`.

- `clock` is a function returning the current time as a number. `deadline` is a number on the same scale.
- Go through `items` in order. Before starting each item, call `clock()`. If it is greater than or equal to `deadline`, stop. Otherwise call `handler(item)` and keep its return value.
- An item that has started always finishes. Never interrupt it.
- Return a tuple `(results, remaining)`. `results` holds the handler results in order. `remaining` is the list of items that were not started, in their original order.
- If the deadline has already passed, nothing runs: return `([], list(items))`.
- If `handler` raises, let the exception go up. Do not catch it.
- Never call the real clock yourself and do not modify `items`.
