**Why this matters.** Time series reports need a bucket per week, month or day, but our data has full timestamps. We have to turn each timestamp into a label that equal weeks share.

**How we get there.**
1. Keep delivered orders only with `WHERE status = 'delivered'`.
2. Turn each timestamp into a week label: `strftime('%Y-%W', created_at)`. Every order of the same week gets the same text, like `'2026-35'`.
3. `GROUP BY week`. SQLite lets us group by the alias we named in the `SELECT`.
4. `COUNT(*)` counts the orders in each week.
5. `ORDER BY week`.

**Check it.** Because the label starts with the year and uses zero-padded numbers, sorting the text also sorts the weeks in time order. The cost is one scan plus a group. The exact week boundaries depend on the dialect; the `%W` rule here starts weeks on Monday.

**Watch out.** Forgetting the status filter, which would count cancelled orders in every week.
