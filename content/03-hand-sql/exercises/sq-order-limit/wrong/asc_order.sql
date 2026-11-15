SELECT order_id, subtotal FROM orders WHERE status = 'delivered' ORDER BY subtotal, order_id LIMIT 23;
