SELECT restaurant_id, order_id, subtotal FROM (
  SELECT restaurant_id, order_id, subtotal,
         ROW_NUMBER() OVER (PARTITION BY restaurant_id ORDER BY subtotal DESC, order_id) AS rn
  FROM orders WHERE status = 'delivered')
WHERE rn = 1 ORDER BY restaurant_id, order_id;
