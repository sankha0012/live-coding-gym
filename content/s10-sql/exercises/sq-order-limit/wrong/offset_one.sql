SELECT order_id, subtotal FROM orders WHERE status = 'delivered' ORDER BY subtotal DESC, order_id LIMIT 23 OFFSET 1;
