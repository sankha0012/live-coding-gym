SELECT order_id, subtotal FROM orders
WHERE subtotal > 140 AND (coupon_code IS NOT NULL OR delivery_fee = 0);
