SELECT order_id, (CASE WHEN subtotal IS NULL THEN 0 ELSE subtotal END) + delivery_fee AS total FROM orders WHERE subtotal IS NULL ORDER BY order_id;
