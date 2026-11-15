**Why this matters.** If we split orders by status, by restaurant or by courier, each split should add back to the total. When it does not, rows were lost or counted twice, usually by a join. A non-zero difference is a clue, not always a bug.

**How we get there.**
1. Count the whole table once: `(SELECT COUNT(*) FROM orders)`. This is `total_orders`.
2. Build the breakdown in an inner query that groups and counts: `SELECT COUNT(*) AS n ... GROUP BY status`. Each row is one group's count.
3. In the outer query take `SUM(n)`. That is `grouped_total`, and the difference is `total_orders - SUM(n)`.
4. For restaurants and couriers, the inner query first does an inner `JOIN` to the table and groups by its id. An order with no match is dropped by the join, so it shows up as a positive difference.
5. Repeat for the three checks, stack with `UNION ALL`, and `ORDER BY check_name`.

**Check it.** Status and restaurant should give 0 on clean data. Courier gives a positive number, because cancelled orders have no courier and the join drops them.

**Watch out.** Read a non-zero difference against the business rules before calling it an error.
