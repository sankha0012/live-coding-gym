SELECT order_id, subtotal FROM (
  SELECT order_id, subtotal, RANK() OVER (ORDER BY subtotal DESC) AS r FROM orders WHERE status = 'delivered'
) WHERE r <= 23 ORDER BY subtotal DESC, order_id;
