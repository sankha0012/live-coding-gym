SELECT r.cuisine, ROUND(SUM(o.subtotal) / COUNT(*), 2) AS avg_subtotal
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' GROUP BY r.cuisine ORDER BY r.cuisine;
