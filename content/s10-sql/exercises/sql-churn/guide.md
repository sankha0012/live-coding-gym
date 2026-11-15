**Why this matters.** Churn means someone was active before and then went quiet. In SQL that is "in set A but not in set B", and we can build it from two small queries.

**How we get there.**
1. Set A is the customers who ordered in August. We pick them with `strftime('%Y-%m', created_at) = '2026-08'`.
2. Set B is the customers who ordered in October, found the same way with `'2026-10'`. We write it as a subquery returning their ids.
3. Keep the August customers with `customer_id NOT IN (...)` and that subquery.
4. A customer may have many August orders, so we count with `COUNT(DISTINCT customer_id)`. One row, one column.

**Check it.** All statuses count as ordering here. A `LEFT JOIN ... IS NULL` gives the same answer. The cost is two scans.

**Watch out.** `NOT IN` returns nothing at all if the subquery contains a NULL. `customer_id` is never NULL here, but it is the first thing to check, and the reason many prefer `NOT EXISTS`.
