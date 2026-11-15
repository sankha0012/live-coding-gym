SELECT order_id, subtotal FROM orders
WHERE status = 'delivered' AND subtotal > 140
  AND NOT (coupon_code IS NULL AND COALESCE(delivery_fee, -1) <> 0);
