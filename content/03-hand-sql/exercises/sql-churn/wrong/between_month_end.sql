SELECT COUNT(DISTINCT customer_id) AS churned FROM orders WHERE created_at BETWEEN '2026-08-01' AND '2026-08-31'
AND customer_id NOT IN (SELECT customer_id FROM orders WHERE created_at BETWEEN '2026-10-01' AND '2026-10-31');
