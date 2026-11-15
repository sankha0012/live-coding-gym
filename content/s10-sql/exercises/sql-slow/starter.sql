SELECT restaurant_id, COUNT(*) AS n, AVG(actual_minutes) AS avg_min
FROM orders
