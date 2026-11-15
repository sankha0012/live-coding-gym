SELECT o.restaurant_id, o.order_id, o.subtotal FROM orders o
WHERE o.subtotal = (SELECT MAX(x.subtotal) FROM orders x WHERE x.restaurant_id = o.restaurant_id AND x.status = 'delivered')
ORDER BY o.restaurant_id, o.order_id;
