WITH o AS (SELECT strftime('%Y-%m', created_at) AS month, LAG(strftime('%Y-%m', created_at)) OVER (ORDER BY created_at) AS prev FROM orders WHERE status = 'delivered')
SELECT month, COUNT(*) AS orders, COUNT(*) - SUM(prev IS NOT NULL AND prev <> month) AS diff FROM o GROUP BY month ORDER BY month;
