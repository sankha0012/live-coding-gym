LAG(revenue) OVER (PARTITION BY city ORDER BY month) gives the previous month of the same city on the row. Growth is (now - before) / before.
