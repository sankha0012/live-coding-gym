**Why this matters.** Sometimes we need to count the groups, not the rows. "How many customers have three or more orders" is a question about customers, but the data is orders.

**How we get there.**
1. Keep delivered orders with `WHERE status = 'delivered'`.
2. `GROUP BY customer_id`, so each customer becomes one group.
3. `HAVING COUNT(*) >= 3` keeps only the groups with three or more orders. We use `HAVING` here, not `WHERE`, because the count only exists after grouping.
4. That gives a list with one row per loyal customer. Wrap it as a subquery and put `SELECT COUNT(*)` around it to count those rows.

**Check it.** The result is a single number, and it is 0 if nobody qualifies, since `COUNT(*)` on an empty list is 0. The cost is one scan and a group.

**Watch out.** Writing `COUNT(*)` straight on the orders: that counts orders, not customers.
