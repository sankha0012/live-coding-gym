SELECT o.restaurant_id, o.order_id, o.subtotal
FROM orders o
WHERE o.status = 'delivered'
  AND ...
