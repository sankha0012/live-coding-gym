**Why this matters.** "The Nth row per group" comes up constantly: a customer's latest order, their second purchase. A plain `GROUP BY` cannot pick a specific row, so we number the rows and pick by number.

**How we get there.**
1. Join `orders` to `customers`, and keep Curitiba customers with delivered orders.
2. Number each customer's orders from newest to oldest: `ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.created_at DESC, o.order_id DESC)`. `PARTITION BY` restarts the count for each customer.
3. The `order_id DESC` tie-break makes "more recent" well defined when two timestamps match.
4. We cannot filter a window result in the same `SELECT`, so we wrap this in a subquery and keep `rn = 2`.
5. `ORDER BY customer_id`.

**Check it.** A customer with one delivered order never gets a row numbered 2, so they drop out on their own. The cost is one sort of the orders.

**Watch out.** Forgetting the tie-break, so two orders with the same timestamp could swap places between runs.
