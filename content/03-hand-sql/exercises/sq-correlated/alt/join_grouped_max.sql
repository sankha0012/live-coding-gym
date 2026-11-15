SELECT o.restaurant_id, o.order_id, o.subtotal
FROM orders o JOIN (SELECT restaurant_id, MAX(subtotal) AS m FROM orders WHERE status = 'delivered' GROUP BY restaurant_id) t
  ON t.restaurant_id = o.restaurant_id AND t.m = o.subtotal
WHERE o.status = 'delivered'
ORDER BY o.restaurant_id, o.order_id;
