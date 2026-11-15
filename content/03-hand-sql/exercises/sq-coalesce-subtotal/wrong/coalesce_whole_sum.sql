SELECT order_id, COALESCE(subtotal + delivery_fee, 0) AS total FROM orders WHERE subtotal IS NULL ORDER BY order_id;
