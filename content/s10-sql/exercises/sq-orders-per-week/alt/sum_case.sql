SELECT strftime('%Y-%W', created_at) AS week, SUM(status = 'delivered') AS orders FROM orders
GROUP BY 1 HAVING SUM(status = 'delivered') > 0 ORDER BY 1;
