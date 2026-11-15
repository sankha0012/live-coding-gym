SELECT r.city, SUM(o.actual_minutes > o.promised_minutes) AS late_orders
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered'
GROUP BY r.city HAVING late_orders > 0
ORDER BY late_orders DESC, r.city;
