SELECT strftime('%Y-%W', created_at) AS week, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY date(created_at) ORDER BY week;
