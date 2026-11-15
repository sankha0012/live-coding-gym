SELECT r.cuisine,
       COUNT(CASE WHEN o.status = 'delivered' THEN 1 END) AS delivered,
       COUNT(CASE WHEN o.status = 'cancelled' THEN 1 END) AS cancelled
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.cuisine ORDER BY r.cuisine;
