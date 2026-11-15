SELECT date(created_at, 'weekday 0', '-6 days') AS week, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY week ORDER BY week;
