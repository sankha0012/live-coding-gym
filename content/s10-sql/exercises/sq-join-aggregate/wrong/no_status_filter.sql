SELECT r.cuisine, COUNT(*) AS orders, ROUND(SUM(o.subtotal), 2) AS revenue
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.cuisine ORDER BY revenue DESC, r.cuisine;
