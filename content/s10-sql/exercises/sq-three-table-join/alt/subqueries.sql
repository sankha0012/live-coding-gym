SELECT o.order_id,
       (SELECT name FROM restaurants r WHERE r.restaurant_id = o.restaurant_id) AS restaurant_name,
       (SELECT name FROM couriers k WHERE k.courier_id = o.courier_id) AS courier_name
FROM orders o
WHERE o.status = 'delivered'
  AND o.restaurant_id IN (SELECT restaurant_id FROM restaurants WHERE cuisine = 'japanese')
  AND o.courier_id IN (SELECT courier_id FROM couriers WHERE vehicle = 'car')
ORDER BY o.order_id;
