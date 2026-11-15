SELECT order_id, subtotal FROM orders
WHERE subtotal > 2 * (SELECT AVG(subtotal) FROM orders WHERE status = 'delivered') ORDER BY order_id;
