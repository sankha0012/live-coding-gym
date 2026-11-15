**Why this matters.** Daily counts jump around, so people smooth them with a 7-day average. The trap is the date filter: the first days in the range need the six days before them, so if we filter early we starve the average.

**How we get there.**
1. Count delivered orders per day with `date(created_at)`, `COUNT(*)` and `GROUP BY date(created_at)`.
2. On top of that grouped result, average the daily counts with a window: `AVG(COUNT(*)) OVER (ORDER BY date(created_at) ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`. Windows run after grouping, so we can average an aggregate.
3. Wrap the `ROUND(..., 2)` around it.
4. Put all of that in a subquery and only then filter `day BETWEEN '2026-10-20' AND '2026-10-31'` in the outer query.
5. Sort by `day`.

**Check it.** The frame counts rows, not calendar days, so a day with no orders would stretch the window. Here that is what the problem asks for. The cost is one group and one sort.

**Watch out.** Filtering the dates in the inner query: the early days of the range then average fewer than seven rows.
