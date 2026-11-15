SELECT o.order_id, r.name AS restaurant_name, k.name AS courier_name
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id JOIN couriers k ON k.courier_id = o.courier_id
WHERE o.status = 'delivered' AND k.vehicle LIKE 'car%' AND r.cuisine = 'japanese' ORDER BY o.order_id;
