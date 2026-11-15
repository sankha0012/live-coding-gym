SELECT restaurant_id, COUNT(actual_minutes) AS n, AVG(actual_minutes) AS avg_min FROM orders WHERE actual_minutes IS NOT NULL
GROUP BY restaurant_id HAVING n >= 40 AND avg_min > 42 ORDER BY avg_min DESC;
