SELECT r.cuisine,
       SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
       SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.cuisine
HAVING SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) >= 18
ORDER BY r.cuisine;
