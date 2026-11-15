SELECT r.cuisine, ROUND(AVG(o.subtotal), 2) AS avg_subtotal
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.cuisine ORDER BY r.cuisine;
