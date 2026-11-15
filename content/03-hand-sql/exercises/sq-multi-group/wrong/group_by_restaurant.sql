SELECT r.city, r.cuisine, COUNT(*) AS delivered_orders
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered'
GROUP BY r.restaurant_id
ORDER BY r.city, r.cuisine;
