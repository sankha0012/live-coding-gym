WITH d AS (SELECT restaurant_id, actual_minutes > promised_minutes AS late FROM orders WHERE status = 'delivered')
SELECT r.cuisine, 1.0 * SUM(d.late) / COUNT(*) AS late_rate FROM d JOIN restaurants r USING (restaurant_id) GROUP BY r.cuisine ORDER BY late_rate DESC;
