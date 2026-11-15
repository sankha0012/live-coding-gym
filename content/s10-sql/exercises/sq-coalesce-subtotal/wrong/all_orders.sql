SELECT order_id, COALESCE(subtotal, 0) + delivery_fee AS total FROM orders ORDER BY order_id;
