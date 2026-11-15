SELECT r.city, COUNT(*) AS late_orders FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' AND o.actual_minutes > o.promised_minutes
GROUP BY r.restaurant_id ORDER BY late_orders DESC, r.city;
