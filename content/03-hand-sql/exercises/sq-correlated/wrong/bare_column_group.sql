SELECT restaurant_id, order_id, MAX(subtotal) AS subtotal FROM orders
WHERE status = 'delivered' GROUP BY restaurant_id ORDER BY restaurant_id, order_id;
