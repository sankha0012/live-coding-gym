**Why this matters.** Duplicate rows inflate counts and revenue. The obvious check, repeated `order_id`, finds nothing here because it is a primary key. So we have to decide what "the same order" means to the business.

**How we get there.**
1. Define the business key: the same customer, the same restaurant and the same calendar day. The date is the first 10 characters of `created_at`, which `date(created_at)` gives us.
2. Start with `FROM orders`. One row per key is the goal, so we `GROUP BY customer_id, restaurant_id, date(created_at)`.
3. Select those three columns plus `COUNT(*) AS n`, and call the date `order_date`.
4. We only want keys that appear more than once. `WHERE` runs before grouping, so it cannot see the count. We use `HAVING COUNT(*) > 1` instead.
5. Sort with `ORDER BY n DESC, customer_id, restaurant_id, order_date`, so the worst offenders come first and ties are stable.

**Check it.** A key with one order never shows up, because `HAVING` removes it. One scan plus a grouping, so linear.

**Watch out.** Putting `COUNT(*) > 1` in `WHERE` fails. Also, two real orders on one day can share the key, so these rows are suspects, not deletions.
