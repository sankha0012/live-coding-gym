SELECT restaurant_id, COUNT(*) AS n, AVG(actual_minutes) AS avg_min FROM orders WHERE status = 'delivered'
GROUP BY restaurant_id HAVING AVG(actual_minutes) > 42 ORDER BY avg_min DESC;
