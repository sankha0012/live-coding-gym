# SQL


<p class="lede">Fifteen moves. The SQL drills run for real against a small delivery database in your browser.</p>
<pre class="code">SELECT city, COUNT(*) AS n, AVG(x) AS avg_x
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered'        -- rows, before grouping
GROUP BY city
HAVING COUNT(*) &gt;= 100              -- groups, after grouping
ORDER BY n DESC LIMIT 10;

AVG(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0 END)     -- a rate
WITH rev AS (...) SELECT ... FROM rev                        -- name your steps
ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC)  -- top N per group
LAG(orders) OVER (ORDER BY month)                            -- previous row
SUM(gmv) OVER (PARTITION BY customer_id ORDER BY created_at) -- running total
COALESCE(coupon_code, 'none');  WHERE x IS NULL              -- never = NULL
WHERE id NOT IN (SELECT ...)  /  LEFT JOIN b ... WHERE b.id IS NULL</pre>
<p>Dates depend on the dialect, so say which one you assume: <code>DATE_TRUNC('month', ts)</code> in Postgres, Databricks and Snowflake; <code>strftime('%Y-%m', ts)</code> in SQLite.</p>
