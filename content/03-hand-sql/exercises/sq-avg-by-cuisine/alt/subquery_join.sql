SELECT r.cuisine, ROUND(AVG(d.subtotal), 2) AS avg_subtotal
FROM restaurants r JOIN (SELECT restaurant_id, subtotal FROM orders WHERE status = 'delivered') d ON d.restaurant_id = r.restaurant_id
GROUP BY r.cuisine ORDER BY r.cuisine;
