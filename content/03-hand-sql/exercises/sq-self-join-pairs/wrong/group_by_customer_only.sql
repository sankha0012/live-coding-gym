SELECT o.customer_id, MIN(o.restaurant_id) AS restaurant_id
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.city IN ('Rio de Janeiro') OR r.cuisine = 'burger'
GROUP BY o.customer_id HAVING COUNT(*) >= 2
ORDER BY o.customer_id;
