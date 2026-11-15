SELECT r.cuisine, 1.0 * COUNT(*) / (SELECT COUNT(*) FROM orders WHERE status = 'delivered') AS late_rate
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id WHERE o.status = 'delivered' AND o.actual_minutes > o.promised_minutes GROUP BY r.cuisine ORDER BY late_rate DESC;
