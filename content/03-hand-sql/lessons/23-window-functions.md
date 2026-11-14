# Window functions

## The problem it solves

`GROUP BY` collapses rows. Sometimes you want to keep every row and add a number that looks at its neighbours: the rank within a city, the previous order, a running total. A window function does this. It adds a column and never removes rows.

## The shape

```
function(...) OVER (PARTITION BY a ORDER BY b ROWS BETWEEN ...)
```

`PARTITION BY` splits the rows into independent groups, like GROUP BY but without collapsing. `ORDER BY` sets the order inside each group. The frame (`ROWS BETWEEN`) says which neighbours the function sees. Window functions run after WHERE and GROUP BY, so you cannot filter on them in the same query level. Wrap them in a CTE.

## The smallest example: the latest order per customer

Tables used: `orders`.

```sql
WITH ranked AS (
    SELECT order_id, customer_id, created_at,
           ROW_NUMBER() OVER (PARTITION BY customer_id
                              ORDER BY created_at DESC, order_id DESC) AS rn
    FROM orders
)
SELECT customer_id, order_id, created_at
FROM ranked
WHERE rn = 1
ORDER BY customer_id
LIMIT 3;
```

Change `rn = 1` to `rn <= 3` for the top three per group. Always add a tie-breaker (`order_id`) so the result is the same on every run.

## Ranking: row_number, rank, dense_rank

With the values 10, 10, 8 ordered descending:

- `ROW_NUMBER` gives 1, 2, 3. Ties get arbitrary different numbers.
- `RANK` gives 1, 1, 3. Ties share a rank and a gap follows.
- `DENSE_RANK` gives 1, 1, 2. Ties share a rank and no gap.

```sql
SELECT customer_id, ROUND(SUM(subtotal)) AS spend,
       RANK() OVER (ORDER BY ROUND(SUM(subtotal)) DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY ROUND(SUM(subtotal)) DESC) AS drnk
FROM orders
GROUP BY customer_id
ORDER BY rnk, customer_id
LIMIT 5;
```

Pick by the wording: "top 3 rows" is ROW_NUMBER, "everyone tied for first" is RANK, "the 3 highest distinct values" is DENSE_RANK.

## Neighbours: lag, lead, first_value

`LAG(x)` is the value from the previous row, `LEAD(x)` from the next row, `FIRST_VALUE(x)` from the first row of the frame.

```sql
SELECT order_id, created_at,
       LAG(subtotal) OVER w AS prev_subtotal,
       LEAD(order_id) OVER w AS next_order,
       FIRST_VALUE(subtotal) OVER w AS first_subtotal
FROM orders
WHERE customer_id = 2
WINDOW w AS (PARTITION BY customer_id ORDER BY created_at, order_id)
ORDER BY created_at, order_id;
```

`WINDOW w AS (...)` names a window so you do not repeat it. Postgres and MySQL support it too; BigQuery does as well. The first row has no previous row, so `LAG` returns NULL. Give a default with `LAG(x, 1, 0)` if you need one.

## Running totals and frames

Add an `ORDER BY` to an aggregate and it becomes a running aggregate:

```sql
SELECT order_id, created_at,
       SUM(subtotal) OVER (PARTITION BY customer_id ORDER BY created_at, order_id) AS running
FROM orders
WHERE customer_id = 2 AND subtotal IS NOT NULL
ORDER BY created_at, order_id;
```

For a moving window, write the frame. A 3-row moving average:

```sql
SELECT order_id,
       AVG(actual_minutes) OVER (ORDER BY created_at, order_id
                                 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg3
FROM orders
WHERE status = 'delivered'
ORDER BY created_at, order_id
LIMIT 5;
```

`ROWS` counts rows. `RANGE` counts values of the ORDER BY column, so rows with equal values are included together. `NTILE(4)` cuts the ordered rows into four equal buckets: `NTILE(4) OVER (ORDER BY spend)`.

## The three traps

1. **Filtering on a window result.** `WHERE rn = 1` in the same SELECT is an error. Put the window in a CTE or subquery and filter outside.
2. **The default frame.** With an `ORDER BY` and no frame, the frame is `RANGE ... UNBOUNDED PRECEDING TO CURRENT ROW`. Rows with the same ORDER BY value are all included, so a running total jumps by several rows at once on ties. Add a unique tie-breaker, or write `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Also `LAST_VALUE` with the default frame returns the current row, not the last one.
3. **Missing tie-breaker.** `ORDER BY created_at` with two equal timestamps lets the database pick any order, and the answer can change between runs. Add a unique column last.

## Say it like this

"I use a window function because I need the row detail and the group context together. I partition by customer and order by time, and I number the rows with ROW_NUMBER. I add the order id as a tie-breaker so the result is deterministic. Then I filter in an outer query, because windows run after WHERE. If the question says ties share a place, I switch to RANK or DENSE_RANK. It is one sort per partition, so the cost is O(n log n)."
