SELECT o.restaurant_id, o.order_id, o.subtotal
FROM orders o JOIN (SELECT restaurant_id, MAX(subtotal) AS m FROM orders WHERE status = 'delivered' GROUP BY restaurant_id) t
  ON o.subtotal = t.m
WHERE o.status = 'delivered'
ORDER BY o.restaurant_id, o.order_id;
