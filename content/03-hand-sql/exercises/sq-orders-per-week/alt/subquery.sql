SELECT week, COUNT(*) AS orders FROM (
  SELECT strftime('%Y-%W', created_at) AS week FROM orders WHERE status = 'delivered'
) GROUP BY week ORDER BY week;
