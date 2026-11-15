**Why this matters.** "Top N" lists are everywhere. The hidden problem is ties: when the 23rd and 24th rows have the same value, the cut-off is ambiguous unless we say how to break the tie.

**How we get there.**
1. Keep only delivered orders with `WHERE status = 'delivered'`. Filtering comes before sorting.
2. Sort by `subtotal DESC`, so the biggest orders come first.
3. Add `order_id` as a second sort key. It only matters when subtotals are equal, and it makes the order fully determined.
4. Cut the list with `LIMIT 23`. LIMIT is applied last, after the sort, so it keeps the first 23 sorted rows.

**Check it.** Without the second key the engine may return either of two tied rows at the edge, and the answer could change between runs. Sorting costs O(n log n), though engines can do top-N faster with a heap.

**Watch out.** Sorting only by `subtotal`, which leaves the tied rows at the cut-off in an arbitrary order.
