SELECT strftime('%Y-%W', created_at) AS week, COUNT(DISTINCT customer_id) AS orders FROM orders WHERE status = 'delivered' GROUP BY week ORDER BY week;
