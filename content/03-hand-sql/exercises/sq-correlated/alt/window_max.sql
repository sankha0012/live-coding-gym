SELECT restaurant_id, order_id, subtotal FROM (
  SELECT restaurant_id, order_id, subtotal, MAX(subtotal) OVER (PARTITION BY restaurant_id) AS m
  FROM orders WHERE status = 'delivered')
WHERE subtotal = m ORDER BY restaurant_id, order_id;
