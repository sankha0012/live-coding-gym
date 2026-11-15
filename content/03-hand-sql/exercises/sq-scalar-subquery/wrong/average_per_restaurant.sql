SELECT o.order_id, o.subtotal FROM orders o
WHERE o.status = 'delivered'
  AND o.subtotal > 2 * (SELECT AVG(p.subtotal) FROM orders p WHERE p.status = 'delivered' AND p.restaurant_id = o.restaurant_id)
ORDER BY o.order_id;
