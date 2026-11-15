**Why this matters.** The point of deduplicating is one row per key. A query that can return two rows for a tie breaks that silently, and the output still looks right on most data.

**How we get there.**
1. Run the query and check `GROUP BY customer_id, restaurant_id HAVING COUNT(*) > 1` on its output. Customer 1 and restaurant 2 appear twice.
2. Look at those two orders: they have the same `created_at`.
3. Cause: `RANK()` gives tied rows the same rank, so both have `rn = 1`.
4. Replace it with `ROW_NUMBER()` and order by `created_at DESC, order_id DESC`. Now the numbers are unique and the tie goes to the higher order_id, as the prompt says.
5. Run again and compare with the reference.

**Check it.** Exactly one row per pair, and for the tied pair the higher order_id is kept.

**Watch out.** `ROW_NUMBER()` without a tie-break is unique but arbitrary among ties, so the result could change between runs.
