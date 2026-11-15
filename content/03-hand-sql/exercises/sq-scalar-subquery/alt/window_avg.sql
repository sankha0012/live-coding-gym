SELECT order_id, subtotal FROM (
  SELECT order_id, subtotal, AVG(subtotal) OVER () AS m FROM orders WHERE status = 'delivered'
) WHERE subtotal > 2 * m ORDER BY order_id;
