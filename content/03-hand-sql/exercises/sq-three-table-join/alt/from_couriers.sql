SELECT o.order_id, r.name AS restaurant_name, k.name AS courier_name
FROM couriers k
JOIN orders o ON o.courier_id = k.courier_id AND o.status = 'delivered'
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE k.vehicle = 'car' AND r.cuisine = 'japanese'
ORDER BY o.order_id;
