SELECT order_id, subtotal + delivery_fee AS total FROM orders WHERE subtotal IS NULL ORDER BY order_id;
