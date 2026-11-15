SELECT r.city, COUNT(*) AS orders, AVG(CASE WHEN o.status = 'cancelled' THEN 1.0 ELSE 0 END) AS cancel_rate
FROM restaurants r LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id GROUP BY r.city ORDER BY orders DESC;
