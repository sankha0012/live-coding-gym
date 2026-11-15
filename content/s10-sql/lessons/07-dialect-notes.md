# Dialect notes: what changes outside SQLite

## The problem it solves

The gym runs SQLite, but the interview may use Postgres, BigQuery or MySQL. The ideas are the same: joins, GROUP BY, windows, CTEs. What changes is a short list of functions and clauses. Say your dialect out loud at the start, and name the one-line change if you know it.

## The smallest example: one query, four spellings

Task: delivered orders per month. In SQLite, which you can run here:

```sql
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS n
FROM orders
WHERE status = 'delivered'
GROUP BY month
ORDER BY month;
```

The month bucket in each dialect:

| Dialect | Month bucket |
|---|---|
| SQLite | `strftime('%Y-%m', ts)` |
| Postgres | `DATE_TRUNC('month', ts)` or `TO_CHAR(ts, 'YYYY-MM')` |
| BigQuery | `DATE_TRUNC(DATE(ts), MONTH)` or `FORMAT_DATE('%Y-%m', DATE(ts))` |
| MySQL | `DATE_FORMAT(ts, '%Y-%m')` |

Everything else in that query stays the same. Note that `GROUP BY month` using an output alias works in SQLite, MySQL, BigQuery and Postgres, but SQL Server does not allow it.

## Date arithmetic

| Task | SQLite | Postgres | BigQuery | MySQL |
|---|---|---|---|---|
| Days between | `julianday(b) - julianday(a)` | `b::date - a::date` | `DATE_DIFF(b, a, DAY)` | `DATEDIFF(b, a)` |
| Add 7 days | `date(x, '+7 days')` | `x + INTERVAL '7 days'` | `DATE_ADD(x, INTERVAL 7 DAY)` | `x + INTERVAL 7 DAY` |
| Current time | `datetime('now')` | `NOW()` | `CURRENT_TIMESTAMP()` | `NOW()` |

Check the argument order every time. `DATEDIFF(b, a)` in MySQL and `DATE_DIFF(b, a, DAY)` in BigQuery both give b minus a, but SQL Server's `DATEDIFF(day, a, b)` takes the start first.

## LIMIT, TOP and friends

`LIMIT n` works in SQLite, Postgres, MySQL and BigQuery. SQL Server uses `SELECT TOP n`, and Oracle uses `FETCH FIRST n ROWS ONLY`, which Postgres also accepts. In MySQL, `LIMIT 5, 10` means offset 5, count 10, which confuses people. Write `LIMIT 10 OFFSET 5` everywhere instead.

## QUALIFY

BigQuery, Snowflake and Databricks have `QUALIFY`, which filters on a window function without a CTE:

```sql
SELECT customer_id, order_id, created_at
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) = 1
```

SQLite, Postgres and MySQL do not have it. This is the portable form, and it runs here:

```sql
WITH r AS (
    SELECT customer_id, order_id, created_at,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC, order_id DESC) AS rn
    FROM orders
)
SELECT customer_id, order_id, created_at FROM r WHERE rn = 1 ORDER BY customer_id LIMIT 3;
```

## FILTER

Postgres and SQLite 3.30 or newer have `FILTER` on aggregates. It is a cleaner version of the CASE trick:

```sql
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled
FROM orders;
```

BigQuery and MySQL do not have it. Use `COUNTIF(status = 'cancelled')` in BigQuery, and `SUM(status = 'cancelled')` in MySQL. The portable form works everywhere: `SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)`.

## The three traps

1. **Integer division.** In SQLite and Postgres, `1 / 2` is 0. In MySQL it is 0.5. In BigQuery `/` gives a float. For a rate, write `1.0 * a / b` or use `AVG(CASE ... 1.0 ...)` and it works everywhere.
2. **Case and quoting.** Postgres folds unquoted names to lower case and uses double quotes for identifiers and single quotes for strings. MySQL uses backticks for identifiers. BigQuery uses backticks for project and table paths. Strings are always single quotes in the standard.
3. **Sorting NULLs and strictness.** Postgres puts NULLs last in ascending order, SQLite puts them first. Postgres, BigQuery and MySQL with strict mode reject a SELECT column that is not grouped. Add `NULLS LAST` in Postgres or `ORDER BY x IS NULL, x` to be portable.

## Say it like this

"I will write this in SQLite syntax, and I know the dialect points. For the month bucket I would use DATE_TRUNC in Postgres or DATE_FORMAT in MySQL. For the latest row per group I use ROW_NUMBER in a CTE, which works everywhere, and in BigQuery I could shorten it with QUALIFY. For a conditional count I use CASE inside SUM, because FILTER is not available in every engine."
