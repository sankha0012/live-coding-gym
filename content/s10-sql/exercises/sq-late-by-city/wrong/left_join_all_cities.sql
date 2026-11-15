SELECT r.city, COUNT(o.order_id) AS late_orders FROM restaurants r
LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id AND o.status = 'delivered' AND o.actual_minutes > o.promised_minutes
GROUP BY r.city ORDER BY late_orders DESC, r.city;
