WITH d AS (SELECT order_id, subtotal FROM orders WHERE status = 'delivered')
SELECT order_id, subtotal FROM d ORDER BY subtotal DESC, order_id ASC LIMIT 23;
