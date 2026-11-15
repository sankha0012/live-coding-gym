---
title: "Dates in SQLite: strftime, date, julianday"
summary: SQLite stores dates as text; use date(), strftime() and julianday() to cut, format and subtract them.
tags: [sql, dates]
---
```sql
SELECT created_at,                                   -- '2026-10-12 23:37:00'
       date(created_at)                 AS day,      -- '2026-10-12'
       strftime('%Y-%m', created_at)    AS month,    -- '2026-10'
       strftime('%H', created_at)       AS hour,     -- '23' (text)
       strftime('%w', created_at)       AS weekday,  -- '0' Sunday ... '6' Saturday
       date(created_at, '+7 days')      AS week_later,
       date(created_at, 'start of month') AS month_start,
       julianday('2026-11-01') - julianday(created_at) AS days_until
FROM orders
LIMIT 3;
```

- Dates are text in ISO format (`YYYY-MM-DD HH:MM:SS`), so `<`, `>` and `ORDER BY` work on them.
- `strftime(format, value)` returns text. The format comes first.
- `julianday(a) - julianday(b)` is the difference in days, with decimals.

<!-- more -->

## Details

SQLite has no date type. The date functions read ISO text and return text (or a number for `julianday`). If the text is not valid ISO, they return NULL.

Main functions: `date(x)` gives `YYYY-MM-DD`, `time(x)` gives `HH:MM:SS`, `datetime(x)` gives both, `strftime(fmt, x)` gives any format, `julianday(x)` gives a day number.

Common format codes: `%Y` year, `%m` month, `%d` day, `%H` hour, `%M` minute, `%S` second, `%w` weekday number, `%W` week of year (Monday first), `%j` day of year.

Modifiers come after the value and apply left to right: `'+1 day'`, `'-3 months'`, `'start of month'`, `'start of year'`, `'weekday 1'` (move forward to the next Monday).

Group by a period by formatting first:

```sql
SELECT strftime('%Y-%m', created_at) AS month,
       COUNT(*) AS orders,
       ROUND(AVG(julianday(date(created_at, 'start of month', '+1 month'))
                 - julianday(created_at)), 1) AS avg_days_to_month_end
FROM orders
GROUP BY month
ORDER BY month;
```

Whole days between two dates: `CAST(julianday(b) - julianday(a) AS INTEGER)`. Multiply the difference by 24 for hours or by 1440 for minutes.

For a date range on a column with a time part, use a half-open range: `created_at >= '2026-10-01' AND created_at < '2026-11-01'`.

`date('now')` is today in UTC. Avoid it in exercises: the answer changes every day.

Dialects: Postgres uses `DATE_TRUNC('month', ts)`, `EXTRACT(HOUR FROM ts)`, `TO_CHAR` and `ts + INTERVAL '7 days'`. BigQuery uses `DATE_TRUNC(d, MONTH)`, `FORMAT_DATE` and `DATE_DIFF(a, b, DAY)`. MySQL uses `DATE_FORMAT` and `DATEDIFF(a, b)`.

## Common mistakes

- Swapping the arguments: `strftime(created_at, '%Y-%m')` returns NULL or nonsense.
- Comparing `strftime('%H', x) > 9`. The result is text; use `CAST(... AS INTEGER)` or compare with `'09'`.
- Subtracting date strings directly: `'2026-10-12' - '2026-10-01'` gives 0 (it subtracts the years).
- Using lower-case `%y` or `%M` for month. `%m` is month, `%M` is minute.
- Using `BETWEEN` with an end date on a datetime column and losing the last day.

## See also

- [GROUP BY and aggregate functions](#/kb/sql-group-by)
- [LAG and LEAD](#/kb/sql-lag-lead)
- [Dialect differences: SQLite, Postgres, BigQuery, MySQL](#/kb/sql-dialects)
- Official docs: https://www.sqlite.org/lang_datefunc.html
