SELECT order_id, subtotal FROM orders
WHERE status = 'delivered' AND subtotal > 2 * (SELECT AVG(subtotal) FROM orders) ORDER BY order_id;
