SELECT COUNT(DISTINCT o.restaurant_id) AS customers, COUNT(*) AS orders
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' AND r.cuisine = 'pizza';
