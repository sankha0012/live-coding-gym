SELECT restaurant_id, COUNT(*) AS n, AVG(actual_minutes) AS avg_min FROM orders
GROUP BY restaurant_id HAVING COUNT(*) >= 40 AND AVG(actual_minutes) > 42 ORDER BY avg_min DESC;
