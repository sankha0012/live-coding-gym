SELECT COUNT(DISTINCT customer_id) AS customers, COUNT(*) AS orders
FROM orders
WHERE status = 'delivered' AND restaurant_id IN (SELECT restaurant_id FROM restaurants WHERE cuisine = 'pizza');
