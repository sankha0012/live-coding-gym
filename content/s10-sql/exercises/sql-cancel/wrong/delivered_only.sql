SELECT r.city, COUNT(*) AS orders, AVG(CASE WHEN o.status = 'cancelled' THEN 1.0 ELSE 0 END) AS cancel_rate
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id WHERE o.status = 'delivered' GROUP BY r.city ORDER BY orders DESC;
