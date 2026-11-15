**Why this matters.** Before trusting a table, we ask how much of it is empty. A column that is 40 percent NULL changes every average built on it. But a NULL is not always an error, so the number tells us where to look.

**How we get there.**
1. Count NULLs in one column. In SQLite `subtotal IS NULL` is 1 or 0, so `SUM(subtotal IS NULL)` is the number of NULLs.
2. Turn that into a rate. Divide by `COUNT(*)`, the number of orders. We multiply by `100.0` rather than `100`, so the division is not an integer division that rounds to zero.
3.
4. We need four columns and the output has one row each. Stack four such SELECTs with `UNION ALL`, which keeps all rows without removing duplicates.
5. Put them in a subquery and filter `WHERE null_pct > 0`, then sort `null_pct DESC, column_name`.

**Check it.** A column with no NULLs gets 0.0 and is filtered out. Linear per column.

**Watch out.** Using `COUNT(col)` or an integer `100` gives the wrong rate. Also, `coupon_code` and cancelled orders' `courier_id` are empty by design, so a high rate is not automatically a bug.
