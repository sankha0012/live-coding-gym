SELECT strftime('%Y-%U', created_at) AS week, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY week ORDER BY week;
