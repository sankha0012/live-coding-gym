---
title: CASE expressions
summary: CASE returns a value chosen by the first condition that is true; it is SQL's if / else.
tags: [sql, expressions]
---
```sql
SELECT order_id,
       actual_minutes,
       CASE
         WHEN actual_minutes IS NULL THEN 'no time'
         WHEN actual_minutes < 30    THEN 'fast'
         WHEN actual_minutes < 45    THEN 'normal'
         ELSE 'slow'
       END AS speed
FROM orders;
```

- Branches are tested top to bottom. The first true `WHEN` wins.
- With no `ELSE`, a row that matches nothing gets NULL.
- Every `CASE` ends with `END`. Add `AS name` after it for the column name.

<!-- more -->

## Details

`CASE` is an expression: it gives one value per row. You can use it anywhere a value is allowed: in `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, and inside aggregates.

There are two forms. The searched form (above) has a full condition in each `WHEN`. The simple form compares one expression with fixed values:

```sql
SELECT name,
       CASE vehicle
         WHEN 'bike' THEN 'no engine'
         WHEN 'car'  THEN 'engine'
         WHEN 'motorbike' THEN 'engine'
         ELSE 'other'
       END AS kind
FROM couriers;
```

The simple form tests with `=`, so it can never match NULL. Use the searched form with `IS NULL` for that.

Because the first match wins, order ranges from the most specific to the most general. With `< 30` before `< 45`, the second branch really means "30 up to 45".

To group by the label, group by the alias or repeat the expression. A `CASE` in `ORDER BY` gives a custom sort order:

```sql
SELECT vehicle, COUNT(*) AS couriers
FROM couriers
GROUP BY vehicle
ORDER BY CASE vehicle WHEN 'bike' THEN 1 WHEN 'motorbike' THEN 2 ELSE 3 END;
```

All branches should return the same type (all text or all numbers).

Dialects: `CASE` is standard and the same everywhere. SQLite also has `IIF(cond, a, b)` for a two-way choice; BigQuery and MySQL have `IF(cond, a, b)`. Postgres has neither, so `CASE` is the portable form.

## Common mistakes

- Forgetting `END`, or writing `END CASE`.
- Putting a wide condition first, so later branches are never reached.
- Writing `WHEN col = NULL` or `CASE col WHEN NULL`. Neither matches. Use `WHEN col IS NULL`.
- Leaving out `ELSE` and then being surprised by NULL labels.
- Mixing text and numbers in the branches.

## See also

- [Conditional aggregation (CASE inside SUM, AVG, COUNT)](#/kb/sql-conditional-aggregation)
- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- [SELECT, WHERE and operators](#/kb/sql-select-where)
- Official docs: https://www.sqlite.org/lang.html
