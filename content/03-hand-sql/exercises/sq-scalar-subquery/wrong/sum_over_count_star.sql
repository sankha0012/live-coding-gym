SELECT order_id, subtotal FROM orders
WHERE status = 'delivered' AND subtotal > 2 * (SELECT SUM(subtotal) * 1.0 / COUNT(*) FROM orders WHERE status = 'delivered') ORDER BY order_id;
