SELECT restaurant_id, COUNT(*) AS n, AVG(COALESCE(actual_minutes, 0)) AS avg_min FROM orders
GROUP BY restaurant_id HAVING COUNT(*) >= 40 AND AVG(COALESCE(actual_minutes, 0)) > 42 ORDER BY avg_min DESC;
