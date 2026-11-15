**Why this matters.** We often want to compare each row with a reference from its own group, such as how much each order differs from the customer's first one. A window function does this without collapsing the rows.

**How we get there.**
1. Filter to the rows that count: customers 22, 117 and 179, delivered, with `subtotal IS NOT NULL`.
2. The NULL filter matters: if a customer's earliest order had no subtotal, `FIRST_VALUE` would return NULL and spoil every row.
3. Define the window once: `WINDOW w AS (PARTITION BY customer_id ORDER BY created_at, order_id)`. Partition means each customer is handled separately, and the order puts the earliest row first.
4. `FIRST_VALUE(subtotal) OVER w` repeats that earliest subtotal on every row of the customer.
5. The difference is plain arithmetic: `ROUND(subtotal - FIRST_VALUE(subtotal) OVER w, 2)`. Sort the final result.

**Check it.** The first order of each customer has a diff of 0. Cost is one sort per partition.

**Watch out.** Forgetting `order_id` in the window order leaves ties in an arbitrary order, so the "first" row may change.
