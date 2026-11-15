SELECT o.order_id,
       (SELECT name FROM customers c WHERE c.customer_id = o.customer_id) AS customer_name,
       (SELECT name FROM restaurants r WHERE r.restaurant_id = o.restaurant_id) AS restaurant_name,
       o.subtotal
FROM orders o
WHERE o.subtotal >= 150
ORDER BY o.order_id;
