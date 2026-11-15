SELECT order_id, subtotal FROM orders
WHERE status = 'delivered' AND subtotal > 2 * (SELECT ROUND(AVG(subtotal)) FROM orders WHERE status = 'delivered') ORDER BY order_id;
