WITH m AS (SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY 1)
SELECT month, orders, orders - (SELECT p.orders FROM m p WHERE p.month < m.month ORDER BY p.month DESC LIMIT 1) AS diff FROM m ORDER BY month;
