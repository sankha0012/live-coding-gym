SELECT r.cuisine, SUM(o.status = 'delivered') AS delivered, SUM(o.status = 'cancelled') AS cancelled
FROM restaurants r JOIN orders o ON o.restaurant_id = r.restaurant_id
GROUP BY r.cuisine ORDER BY r.cuisine;
