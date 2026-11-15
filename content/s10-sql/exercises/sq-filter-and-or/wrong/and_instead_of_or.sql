SELECT order_id, subtotal FROM orders
WHERE status = 'delivered' AND subtotal > 140 AND (coupon_code IS NOT NULL AND delivery_fee = 0);
