SELECT order_id, subtotal FROM orders
WHERE status = 'delivered' AND subtotal > 140 AND ((coupon_code IS NOT NULL AND coupon_code <> '') OR delivery_fee = 0);
