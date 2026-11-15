SELECT r.cuisine, SUM(CASE WHEN o.actual_minutes > o.promised_minutes THEN 1 ELSE 0 END) / COUNT(*) AS late_rate
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id WHERE o.status = 'delivered' GROUP BY r.cuisine ORDER BY late_rate DESC;
