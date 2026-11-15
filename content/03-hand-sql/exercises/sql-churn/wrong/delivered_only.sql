SELECT COUNT(DISTINCT customer_id) AS churned FROM orders WHERE status = 'delivered' AND strftime('%Y-%m', created_at) = '2026-08'
AND customer_id NOT IN (SELECT customer_id FROM orders WHERE status = 'delivered' AND strftime('%Y-%m', created_at) = '2026-10');
