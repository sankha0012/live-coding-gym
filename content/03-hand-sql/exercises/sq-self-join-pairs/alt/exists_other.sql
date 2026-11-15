SELECT DISTINCT o.customer_id, o.restaurant_id
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.city = 'Rio de Janeiro' AND r.cuisine = 'burger'
  AND EXISTS (SELECT 1 FROM orders p WHERE p.customer_id = o.customer_id AND p.restaurant_id = o.restaurant_id AND p.order_id <> o.order_id)
ORDER BY o.customer_id, o.restaurant_id;
