SELECT r.city, COUNT(*) AS orders, SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) AS cancel_rate
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id GROUP BY r.city ORDER BY orders DESC;
