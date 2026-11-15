SELECT o.order_id, c.name AS customer_name, r.name AS restaurant_name, o.subtotal
FROM orders o JOIN customers c ON c.customer_id = o.customer_id JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.subtotal >= 150 AND o.status = 'delivered' ORDER BY o.order_id;
