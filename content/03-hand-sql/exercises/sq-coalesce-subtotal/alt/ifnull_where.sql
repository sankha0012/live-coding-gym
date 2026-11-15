SELECT order_id, IFNULL(subtotal, 0) + delivery_fee AS total FROM orders WHERE subtotal IS NULL ORDER BY order_id;
