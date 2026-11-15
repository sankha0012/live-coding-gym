SELECT r.cuisine,
       SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
       SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
JOIN couriers c ON c.courier_id = o.courier_id
GROUP BY r.cuisine ORDER BY r.cuisine;
