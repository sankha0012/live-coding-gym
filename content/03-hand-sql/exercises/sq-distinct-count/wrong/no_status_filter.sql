SELECT COUNT(DISTINCT o.customer_id) AS customers, COUNT(*) AS orders
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.cuisine = 'pizza';
