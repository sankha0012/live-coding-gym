# NULLs, dates and de-duplication

## The problem it solves

Real data has gaps, text dates and duplicate rows. Three small areas cause most wrong answers in SQL interviews: NULL logic, date arithmetic, and keeping one row per key.

## NULLs: the smallest example

Tables used: `orders`.

NULL means unknown, not zero and not empty. Any comparison with NULL is unknown, which acts like false in a WHERE.

```sql
SELECT COUNT(*) AS all_rows,
       COUNT(subtotal) AS with_subtotal,
       COUNT(coupon_code) AS with_coupon,
       SUM(subtotal IS NULL) AS missing_subtotal
FROM orders;
```

`COUNT(*)` counts rows. `COUNT(col)` counts rows where the column is not NULL. `COUNT(DISTINCT col)` counts distinct non-NULL values. To test for NULL use `IS NULL` and `IS NOT NULL`, never `= NULL`.

`COALESCE(a, b, ...)` returns the first non-NULL argument:

```sql
SELECT order_id,
       COALESCE(subtotal, 0) + delivery_fee AS gmv,
       COALESCE(coupon_code, 'none') AS coupon
FROM orders
WHERE subtotal IS NULL OR order_id = 100001
ORDER BY order_id
LIMIT 4;
```

Decide first whether a missing value means zero. For a sum of money it often does. For an average of minutes it does not, because a zero would drag the average down.

## Dates in SQLite

The dataset stores dates as text like `2026-10-12 23:37:00`. That format sorts correctly as text, which is why SQLite can work with it. The functions:

```sql
SELECT order_id,
       created_at,
       strftime('%Y-%m', created_at) AS month,
       strftime('%Y-%W', created_at) AS week,
       date(created_at) AS day,
       CAST(strftime('%w', created_at) AS INTEGER) AS weekday
FROM orders
ORDER BY order_id
LIMIT 3;
```

`%W` is the week of the year starting on Monday, `%w` is the weekday with 0 for Sunday. To count days between two dates, use `julianday`, which turns a date into a number of days:

```sql
SELECT customer_id,
       CAST(julianday('2026-11-14') - julianday(signup_date) AS INTEGER) AS days_since_signup
FROM customers
ORDER BY customer_id
LIMIT 3;
```

For "the last 7 days from a fixed day" write `created_at >= date('2026-10-31', '-7 days')`. Use a fixed date in the query, not `'now'`, so the answer is the same tomorrow.

## De-duplication with row_number

Duplicates mean several rows for one key, and you keep one. Number the rows inside each key and keep number one. You decide which one with the `ORDER BY`.

```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id
                              ORDER BY created_at DESC, order_id DESC) AS rn
    FROM orders
)
SELECT order_id, customer_id, created_at
FROM ranked
WHERE rn = 1
ORDER BY customer_id
LIMIT 3;
```

To only see which keys are duplicated, use `GROUP BY key HAVING COUNT(*) > 1`. `SELECT DISTINCT` removes only rows that are identical in every selected column, so it does not pick "the latest".

## The three traps

1. **`= NULL` and NOT IN with NULL.** `WHERE coupon_code = NULL` returns nothing. Write `IS NULL`. In the same family, `NOT IN (list with NULL)` returns nothing, so use `NOT EXISTS`.
2. **COUNT(*) versus COUNT(col), and AVG over gaps.** A "number of orders" must be `COUNT(*)`; `COUNT(subtotal)` silently drops the 7 orders with no subtotal. And `AVG(col)` ignores NULLs, so state whether that is what the question wants. Also, `SUM` over no rows is NULL, so wrap it: `COALESCE(SUM(x), 0)`.
3. **Date text and boundaries.** `created_at <= '2026-10-31'` drops everything on the 31st after midnight, because `'2026-10-31 08:00:00'` is greater than `'2026-10-31'`. Use a half-open range: `>= '2026-10-01' AND < '2026-11-01'`. And the week number from `%W` restarts each year, so group by year and week together.

## Say it like this

"I first check which columns can be NULL. I use COUNT(*) for the number of orders and COALESCE where a missing subtotal should count as zero. For dates I use strftime for the month bucket and julianday for the difference in days, and I use a half-open range so the last day is not cut off. To keep one row per customer I number the rows by newest first, with the order id as a tie-breaker, and keep row number one."
