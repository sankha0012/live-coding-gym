SELECT r.city, COUNT(*) AS orders, COUNT(o.status = 'cancelled') * 1.0 / COUNT(*) AS cancel_rate
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id GROUP BY r.city ORDER BY orders DESC;
