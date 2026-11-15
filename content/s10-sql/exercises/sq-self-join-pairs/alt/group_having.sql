SELECT o.customer_id, o.restaurant_id
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.city = 'Rio de Janeiro' AND r.cuisine = 'burger'
GROUP BY o.customer_id, o.restaurant_id HAVING COUNT(*) >= 2
ORDER BY o.customer_id, o.restaurant_id;
