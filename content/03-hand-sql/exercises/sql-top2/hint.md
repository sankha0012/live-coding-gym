CTE for revenue, then ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) AS rn in a subquery, then WHERE rn <= 2 outside.
