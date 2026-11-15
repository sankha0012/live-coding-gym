SELECT order_id, subtotal FROM (
  SELECT order_id, subtotal, ROW_NUMBER() OVER (ORDER BY subtotal DESC, order_id) AS rn
  FROM orders WHERE status = 'delivered'
) WHERE rn <= 23 ORDER BY rn;
