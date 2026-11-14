SELECT DISTINCT a.customer_id, a.restaurant_id
FROM orders a
JOIN orders b ON b.customer_id = a.customer_id
             AND b.restaurant_id = a.restaurant_id
             AND b.order_id > a.order_id
JOIN restaurants r ON r.restaurant_id = a.restaurant_id
WHERE r.city = 'Rio de Janeiro' AND r.cuisine = 'burger'
ORDER BY a.customer_id, a.restaurant_id;
