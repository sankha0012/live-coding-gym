SELECT COUNT(DISTINCT customer_id) AS churned FROM orders WHERE strftime('%Y-%m', created_at) = '2026-08'
AND customer_id NOT IN (SELECT customer_id FROM orders WHERE strftime('%Y-%m', created_at) = '2026-09');
