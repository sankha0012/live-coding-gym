SELECT r.city, r.cuisine, SUM(t.n) AS delivered_orders
FROM (SELECT restaurant_id, COUNT(*) AS n FROM orders WHERE status = 'delivered' GROUP BY restaurant_id) t
JOIN restaurants r ON r.restaurant_id = t.restaurant_id
GROUP BY r.city, r.cuisine
ORDER BY r.city, r.cuisine;
