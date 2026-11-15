SELECT r.cuisine, AVG(CASE WHEN o.actual_minutes > o.promised_minutes THEN 1.0 ELSE 0 END) AS late_rate
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id GROUP BY r.cuisine ORDER BY late_rate DESC;
