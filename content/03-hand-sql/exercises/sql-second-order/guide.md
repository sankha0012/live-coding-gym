**Why this matters.** Time between a customer's first and second purchase tells you how fast new customers come back. We need each customer's first and second order side by side, and a table gives them to us one per row.

**How we get there.**
1. In a CTE, keep delivered orders and number each customer's orders: `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at)`. The oldest gets 1, the next gets 2.
2. Join that CTE to itself on the same `customer_id`, with `a.n = 1` and `b.n = 2`. Now each row holds a customer's first and second order.
3. Subtracting two text timestamps does not give days, so we use `julianday(b.created_at) - julianday(a.created_at)`, which gives days.
4. `AVG` of that gives one number.

**Check it.** The inner join drops customers who have only one order, since they have no row with `n = 2`. That is what the problem wants. The cost is one sort and a join on the customer.

**Watch out.** Using a `LEFT JOIN`, which keeps one-order customers with NULL and is harmless for `AVG` but hides the intent.
