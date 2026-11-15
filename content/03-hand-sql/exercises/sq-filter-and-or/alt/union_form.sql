SELECT order_id, subtotal FROM orders WHERE status = 'delivered' AND subtotal > 140 AND coupon_code IS NOT NULL
UNION
SELECT order_id, subtotal FROM orders WHERE status = 'delivered' AND subtotal > 140 AND delivery_fee = 0;
