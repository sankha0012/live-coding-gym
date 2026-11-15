SELECT strftime('%Y-%W', created_at) AS week, COUNT(*) AS orders FROM orders GROUP BY week ORDER BY week;
