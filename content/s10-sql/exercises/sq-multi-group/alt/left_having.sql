SELECT r.city, r.cuisine, COUNT(o.order_id) AS delivered_orders
FROM restaurants r LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id AND o.status = 'delivered'
GROUP BY r.city, r.cuisine
HAVING COUNT(o.order_id) > 0
ORDER BY r.city, r.cuisine;
