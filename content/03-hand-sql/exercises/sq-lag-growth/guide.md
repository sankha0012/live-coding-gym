**Why this matters.** Growth compares a period with the one before it. SQL rows do not know their neighbours, so we use a window function to bring the previous row onto the current one.

**How we get there.**
1. In a CTE `m`, join orders to restaurants, keep delivered orders, and group by city and month, where `strftime('%Y-%m', created_at)` gives the month. `SUM(subtotal)` is the revenue.
2. We now have one row per city and month. Define `WINDOW w AS (PARTITION BY city ORDER BY month)`.
3. `LAG(revenue) OVER w` returns the previous month of the same city. The partition stops one city from borrowing another's numbers.
4. Growth is `100.0 * (revenue - LAG(revenue) OVER w) / LAG(revenue) OVER w`, rounded to 1 decimal.
5. Sort by city and month.

**Check it.** A city's first month has no previous row, so LAG is NULL and so is the growth. A previous revenue of 0 would be a division problem in real life; here SQLite returns NULL.

**Watch out.** Dropping `PARTITION BY city` makes each city's first month compare against another city.
