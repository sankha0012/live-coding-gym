SELECT restaurant_id, n, avg_min FROM (SELECT restaurant_id, COUNT(*) AS n, AVG(actual_minutes) AS avg_min FROM orders WHERE status = 'delivered' GROUP BY restaurant_id)
WHERE n >= 40 AND avg_min > 42 ORDER BY avg_min DESC;
