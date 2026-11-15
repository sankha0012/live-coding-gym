SELECT r.cuisine, COUNT(*) AS orders, ROUND(SUM(o.subtotal), 2) AS revenue
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' GROUP BY r.cuisine ORDER BY orders DESC, r.cuisine;
