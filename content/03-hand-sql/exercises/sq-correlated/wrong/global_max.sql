SELECT o.restaurant_id, o.order_id, o.subtotal FROM orders o
WHERE o.status = 'delivered'
  AND o.subtotal = (SELECT MAX(x.subtotal) FROM orders x WHERE x.status = 'delivered')
ORDER BY o.restaurant_id, o.order_id;
