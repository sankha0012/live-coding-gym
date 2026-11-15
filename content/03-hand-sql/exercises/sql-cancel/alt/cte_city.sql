WITH x AS (SELECT (SELECT city FROM restaurants r WHERE r.restaurant_id = o.restaurant_id) AS city, status FROM orders o)
SELECT city, COUNT(*) AS n, COUNT(CASE WHEN status = 'cancelled' THEN 1 END) * 1.0 / COUNT(*) AS rate FROM x GROUP BY city ORDER BY n DESC;
