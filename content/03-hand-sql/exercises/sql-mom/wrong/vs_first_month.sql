WITH m AS (SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY month)
SELECT month, orders, orders - FIRST_VALUE(orders) OVER (ORDER BY month) AS diff FROM m ORDER BY month;
