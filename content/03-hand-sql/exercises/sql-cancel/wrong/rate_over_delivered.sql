SELECT r.city, COUNT(*) AS orders, 1.0 * SUM(o.status = 'cancelled') / SUM(o.status = 'delivered') AS cancel_rate
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id GROUP BY r.city ORDER BY orders DESC;
