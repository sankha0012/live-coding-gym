SELECT r.city, r.cuisine, COUNT(*) AS delivered_orders
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.city, r.cuisine
ORDER BY r.city, r.cuisine;
