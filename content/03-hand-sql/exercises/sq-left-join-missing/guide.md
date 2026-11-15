**Why this matters.** "Who never did X" is one of the most common questions in analytics: customers with no orders, users with no logins. The trap is that an ordinary join only returns rows that match, so the people you want are exactly the ones it throws away.

**How we get there.**
1. Start from `customers`, because they are the rows we must keep, even with no match.
2. `LEFT JOIN orders` on `customer_id`. Every customer survives, and a customer with no orders gets NULL in all the order columns.
3. Keep only the Curitiba customers with `WHERE c.city = 'Curitiba'`.
4. Add `AND o.order_id IS NULL`. A real order always has an id, so NULL there means the join found nothing. We must use `IS NULL`, since `= NULL` is never true.
5. Sort with `ORDER BY c.customer_id`.

**Check it.** A customer with several orders produces several joined rows, but none have a NULL id, so they all disappear. A customer with no orders produces exactly one row. The cost is one pass over the join.

**Watch out.** Putting the NULL test in the `ON` clause, or writing `= NULL`, instead of testing it in `WHERE` after the join.
